#!/usr/bin/env python3
"""Run registry-driven runtime surface guard checks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


@dataclass(frozen=True)
class GuardSurface:
    name: str
    exposure: str
    trigger_prefixes: tuple[str, ...]
    protected_source_roots: tuple[str, ...]
    banned_phrases: tuple[str, ...]
    focused_tests: tuple[str, ...]
    live_commands: tuple[str, ...]


@dataclass(frozen=True)
class GuardFinding:
    surface: str
    detail: str
    blocking: bool


def load_surfaces(registry_path: Path) -> list[GuardSurface]:
    spec = spec_from_file_location("runtime_surface_registry", registry_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load registry: {registry_path}")
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    raw_surfaces = getattr(module, "SURFACES", [])
    surfaces: list[GuardSurface] = []
    for raw in raw_surfaces:
        surfaces.append(
            GuardSurface(
                name=raw["name"],
                exposure=raw["exposure"],
                trigger_prefixes=tuple(raw.get("trigger_prefixes", ())),
                protected_source_roots=tuple(raw.get("protected_source_roots", ())),
                banned_phrases=tuple(raw.get("banned_phrases", ())),
                focused_tests=tuple(raw.get("focused_tests", ())),
                live_commands=tuple(raw.get("live_commands", ())),
            )
        )
    return surfaces


def surface_matches(surface: GuardSurface, changed_paths: list[str], mode: str) -> bool:
    if mode in {"staged-check", "push-check", "live-smoke"} and surface.exposure != "active_default_user_path":
        return False
    if mode == "candidate-audit" and surface.exposure != "candidate_incubator_service":
        return False
    return any(
        changed.startswith(prefix) for changed in changed_paths for prefix in surface.trigger_prefixes
    )


def iter_text_files(root: Path, relative_root: str) -> list[Path]:
    target = root / relative_root
    if target.is_file():
        return [target]
    if not target.exists():
        return []
    return [path for path in target.rglob("*") if path.is_file()]


def scan_banned_phrases(root: Path, surface: GuardSurface, *, blocking: bool) -> list[GuardFinding]:
    findings: list[GuardFinding] = []
    for relative_root in surface.protected_source_roots:
        for path in iter_text_files(root, relative_root):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for phrase in surface.banned_phrases:
                if phrase in text:
                    findings.append(
                        GuardFinding(
                            surface=surface.name,
                            detail=f"banned phrase '{phrase}' found in {path.relative_to(root)}",
                            blocking=blocking,
                        )
                    )
    return findings


def run_commands(commands: tuple[str, ...], root: Path, surface: GuardSurface, *, blocking: bool, dry_run: bool) -> list[GuardFinding]:
    findings: list[GuardFinding] = []
    for command in commands:
        if dry_run:
            findings.append(
                GuardFinding(surface=surface.name, detail=f"dry-run: {command}", blocking=False)
            )
            continue
        completed = subprocess.run(command, cwd=root, shell=True, text=True)
        if completed.returncode != 0:
            findings.append(
                GuardFinding(
                    surface=surface.name,
                    detail=f"command failed ({completed.returncode}): {command}",
                    blocking=blocking,
                )
            )
    return findings


def run_guard_mode(
    *,
    root: Path,
    registry_path: Path,
    mode: str,
    changed_paths: list[str],
    dry_run: bool = False,
) -> list[GuardFinding]:
    findings: list[GuardFinding] = []
    for surface in load_surfaces(registry_path):
        if not surface_matches(surface, changed_paths, mode):
            continue

        if mode == "candidate-audit":
            findings.extend(scan_banned_phrases(root, surface, blocking=False))
            findings.extend(run_commands(surface.focused_tests, root, surface, blocking=False, dry_run=dry_run))
            continue

        findings.extend(scan_banned_phrases(root, surface, blocking=True))
        if mode in {"staged-check", "push-check"}:
            findings.extend(run_commands(surface.focused_tests, root, surface, blocking=True, dry_run=dry_run))
        if mode in {"live-smoke", "push-check"}:
            findings.extend(run_commands(surface.live_commands, root, surface, blocking=True, dry_run=dry_run))
    return findings


def _paths_for_command(command: list[str], root: Path) -> list[str]:
    completed = subprocess.run(command, check=True, capture_output=True, text=True, cwd=root)
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def working_tree_dirty(root: Path) -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
        cwd=root,
    )
    return bool(completed.stdout.strip())


def get_changed_paths(
    root: Path,
    *,
    staged: bool,
    commit_ranges: tuple[str, ...] = (),
    commit_shas: tuple[str, ...] = (),
) -> list[str]:
    if commit_ranges or commit_shas:
        paths: list[str] = []
        for commit_range in commit_ranges:
            paths.extend(_paths_for_command(["git", "diff", "--name-only", commit_range], root))

        for commit_sha in commit_shas:
            rev_list = _paths_for_command(["git", "rev-list", commit_sha, "--not", "--remotes"], root)
            if not rev_list:
                rev_list = [commit_sha]
            for revision in rev_list:
                paths.extend(
                    _paths_for_command(
                        ["git", "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", revision],
                        root,
                    )
                )

        return list(dict.fromkeys(paths))

    if staged:
        return _paths_for_command(["git", "diff", "--cached", "--name-only"], root)

    upstream_check = subprocess.run(
        ["git", "rev-parse", "--verify", "@{upstream}"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if upstream_check.returncode == 0:
        command = ["git", "diff", "--name-only", "@{upstream}...HEAD"]
    else:
        command = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]
    return _paths_for_command(command, root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run runtime surface guardrails")
    parser.add_argument("mode", choices=("staged-check", "candidate-audit", "live-smoke", "push-check"))
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(".github/runtime_surface_registry.py"),
        help="registry file path",
    )
    parser.add_argument("--changed-path", action="append", default=[], help="explicit changed path")
    parser.add_argument("--commit-range", action="append", default=[], help="explicit commit range for push checks")
    parser.add_argument("--commit-sha", action="append", default=[], help="tip commit sha for first-push checks")
    parser.add_argument("--dry-run", action="store_true", help="report commands without running them")
    args = parser.parse_args()

    root = args.root.resolve()
    registry = (root / args.registry).resolve() if not args.registry.is_absolute() else args.registry
    changed_paths = list(args.changed_path)
    if args.mode == "push-check" and (args.commit_range or args.commit_sha) and working_tree_dirty(root):
        print("runtime surface push-check requires a clean working tree")
        return 1

    if not changed_paths:
        changed_paths = get_changed_paths(
            root,
            staged=args.mode == "staged-check",
            commit_ranges=tuple(args.commit_range),
            commit_shas=tuple(args.commit_sha),
        )

    findings = run_guard_mode(
        root=root,
        registry_path=registry,
        mode=args.mode,
        changed_paths=changed_paths,
        dry_run=args.dry_run,
    )

    blocking = [finding for finding in findings if finding.blocking]
    if not findings:
        print(f"runtime surface {args.mode} passed")
        return 0

    print(f"runtime surface {args.mode} findings")
    for finding in findings:
        prefix = "ERROR" if finding.blocking else "WARN"
        print(f"[{prefix}] {finding.surface}: {finding.detail}")

    if blocking:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
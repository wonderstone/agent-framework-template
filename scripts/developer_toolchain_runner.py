#!/usr/bin/env python3
"""List, inspect, and run declared Developer Toolchain surfaces."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_validate_template_module():
    module_path = REPO_ROOT / "scripts" / "validate_template.py"
    spec = spec_from_file_location("validate_template_for_toolchain_runner", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATE_TEMPLATE = _load_validate_template_module()
DeveloperToolchainEntry = VALIDATE_TEMPLATE.DeveloperToolchainEntry
parse_developer_toolchain_entries = VALIDATE_TEMPLATE._parse_developer_toolchain_entries


@dataclass(frozen=True)
class RunResult:
    surface: str
    scope: str
    declared_status: str
    command_or_source: str
    fallback_or_stop: str
    outcome: str
    exit_code: str
    evidence_summary: str


def _load_entries(root: Path) -> list[DeveloperToolchainEntry]:
    project_context = root / ".github" / "instructions" / "project-context.instructions.md"
    if not project_context.is_file():
        raise SystemExit("project context file is missing")
    _, _, entries = parse_developer_toolchain_entries(project_context.read_text(encoding="utf-8"))
    if not entries:
        raise SystemExit("Developer Toolchain section has no structured entries")
    return entries


def _manifest_allows_known_broken_override(root: Path) -> bool:
    manifest_path = root / ".github" / "agent-framework-manifest.json"
    if not manifest_path.is_file():
        return True
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    contract = manifest.get("developer_toolchain_runner_contract")
    if not isinstance(contract, dict):
        return True
    return bool(contract.get("allow_known_broken_override", True))


def _select_entry(entries: list[DeveloperToolchainEntry], target: str) -> DeveloperToolchainEntry:
    normalized = target.strip()
    exact_matches = [entry for entry in entries if entry.surface == normalized]
    if len(exact_matches) == 1:
        return exact_matches[0]
    if len(exact_matches) > 1:
        raise SystemExit(f"multiple exact Developer Toolchain surfaces matched: {target}")

    kind_matches = [entry for entry in entries if entry.surface_kind == normalized]
    if len(kind_matches) == 1:
        return kind_matches[0]
    if len(kind_matches) > 1:
        labels = ", ".join(entry.surface for entry in kind_matches)
        raise SystemExit(
            f"surface kind '{target}' is ambiguous; choose one of: {labels}"
        )
    raise SystemExit(f"no matching Developer Toolchain surface found for: {target}")


def _build_receipt_id() -> str:
    return datetime.now(timezone.utc).strftime("toolchain-run-%Y%m%dT%H%M%SZ")


def _resolve_output(root: Path, output: Path | None, receipt_id: str) -> Path:
    if output is not None:
        return output.resolve()
    return root / "tmp" / "toolchain_run_receipts" / f"{receipt_id}.md"


def _summarize_output(completed: subprocess.CompletedProcess[str]) -> str:
    combined = "\n".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part and part.strip()
    ).strip()
    if not combined:
        return "Command produced no output."
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    return " | ".join(lines[:3])[:240]


def _run_entry(
    entry: DeveloperToolchainEntry,
    *,
    root: Path,
    timeout: int,
    allow_known_broken: bool,
) -> RunResult:
    command = entry.command_or_source
    if entry.status == "not-applicable":
        return RunResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            outcome="not-applicable",
            exit_code="n/a",
            evidence_summary="Surface is marked not-applicable in the project adapter.",
        )
    if command.lower() == "none":
        return RunResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            outcome="skipped-explicit-none",
            exit_code="n/a",
            evidence_summary="Surface is explicitly set to none.",
        )
    if entry.status == "known-broken" and not allow_known_broken:
        return RunResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            outcome="skipped-known-broken",
            exit_code="n/a",
            evidence_summary="Known-broken surfaces require --allow-known-broken before execution.",
        )

    completed = subprocess.run(
        command,
        cwd=root,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return RunResult(
        surface=entry.surface,
        scope=entry.scope,
        declared_status=entry.status,
        command_or_source=command,
        fallback_or_stop=entry.fallback_or_stop,
        outcome="success" if completed.returncode == 0 else "failure",
        exit_code=str(completed.returncode),
        evidence_summary=_summarize_output(completed),
    )


def _render_receipt(template: str, *, receipt_id: str, generated_at: str, repository_root: Path, result: RunResult) -> str:
    rendered = template
    replacements = {
        "[receipt-id]": receipt_id,
        "[generated-at]": generated_at,
        "[repository-root]": str(repository_root),
        "[surface]": result.surface,
        "[scope]": result.scope,
        "[declared-status]": result.declared_status,
        "[command-or-source]": result.command_or_source,
        "[fallback-or-stop]": result.fallback_or_stop,
        "[success | failure | skipped-known-broken | skipped-explicit-none | not-applicable]": result.outcome,
        "[exit-code]": result.exit_code,
        "[short-summary]": result.evidence_summary,
    }
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered.rstrip() + "\n"


def _print_table(entries: list[DeveloperToolchainEntry]) -> None:
    print("| Surface | Scope | Status | Command or source | Fallback or stop |")
    print("|---|---|---|---|---|")
    for entry in entries:
        print(
            f"| {entry.surface} | {entry.scope} | {entry.status} | {entry.command_or_source} | {entry.fallback_or_stop} |"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run declared Developer Toolchain surfaces")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to inspect")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-surfaces", help="List declared Developer Toolchain surfaces")

    show_parser = subparsers.add_parser("show-surface", help="Show one declared surface")
    show_parser.add_argument("--surface", required=True)

    run_parser = subparsers.add_parser("run-surface", help="Run one declared surface and write a receipt")
    run_parser.add_argument("--surface", required=True)
    run_parser.add_argument("--timeout", type=int, default=120)
    run_parser.add_argument("--receipt-id")
    run_parser.add_argument("--output", type=Path)
    run_parser.add_argument("--allow-known-broken", action="store_true")

    args = parser.parse_args()
    root = args.root.resolve()
    entries = _load_entries(root)
    manifest_allows_override = _manifest_allows_known_broken_override(root)

    if args.command == "list-surfaces":
        _print_table(entries)
        return 0

    entry = _select_entry(entries, args.surface)
    if args.command == "show-surface":
        print(f"Surface: {entry.surface}")
        print(f"Scope: {entry.scope}")
        print(f"Status: {entry.status}")
        print(f"Command or source: {entry.command_or_source}")
        print(f"Fallback or stop: {entry.fallback_or_stop}")
        if entry.notes:
            print(f"Notes: {entry.notes}")
        return 0

    if args.allow_known_broken and not manifest_allows_override:
        raise SystemExit("manifest policy disallows known-broken overrides for the toolchain runner")

    result = _run_entry(
        entry,
        root=root,
        timeout=args.timeout,
        allow_known_broken=args.allow_known_broken and manifest_allows_override,
    )
    receipt_id = args.receipt_id or _build_receipt_id()
    output_path = _resolve_output(root, args.output, receipt_id)
    template = (root / "templates" / "developer_toolchain_run_receipt.template.md").read_text(encoding="utf-8")
    rendered = _render_receipt(
        template,
        receipt_id=receipt_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        repository_root=root,
        result=result,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Probe declared Developer Toolchain surfaces and write a receipt."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_validate_template_module():
    module_path = REPO_ROOT / "scripts" / "validate_template.py"
    spec = spec_from_file_location("validate_template_for_toolchain_probe", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATE_TEMPLATE = _load_validate_template_module()
DeveloperToolchainEntry = VALIDATE_TEMPLATE.DeveloperToolchainEntry
parse_developer_toolchain_entries = VALIDATE_TEMPLATE._parse_developer_toolchain_entries


@dataclass(frozen=True)
class ProbeResult:
    surface: str
    scope: str
    declared_status: str
    probe_outcome: str
    exit_code: str
    command_or_source: str
    fallback_or_stop: str
    evidence_summary: str


def _resolve_output(root: Path, output: Path | None, receipt_id: str) -> Path:
    if output is not None:
        return output.resolve()
    return root / "tmp" / "toolchain_probe_receipts" / f"{receipt_id}.md"


def _build_receipt_id() -> str:
    return datetime.now(timezone.utc).strftime("toolchain-probe-%Y%m%dT%H%M%SZ")


def _select_entries(
    entries: list[DeveloperToolchainEntry],
    selected_surfaces: list[str],
) -> list[DeveloperToolchainEntry]:
    if not selected_surfaces:
        return entries
    requested = {value.strip() for value in selected_surfaces}
    selected = [
        entry
        for entry in entries
        if entry.surface in requested or entry.surface_kind in requested
    ]
    if not selected:
        raise SystemExit(f"no matching Developer Toolchain surfaces found for: {', '.join(selected_surfaces)}")
    return selected


def _summarize_output(completed: subprocess.CompletedProcess[str]) -> str:
    combined = "\n".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part and part.strip()
    ).strip()
    if not combined:
        return "Command produced no output."
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    summary = " | ".join(lines[:3])
    return summary[:240]


def _probe_entry(
    entry: DeveloperToolchainEntry,
    *,
    root: Path,
    timeout: int,
    include_known_broken: bool,
) -> ProbeResult:
    command = entry.command_or_source
    if entry.status == "not-applicable":
        return ProbeResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            probe_outcome="not-applicable",
            exit_code="n/a",
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            evidence_summary="Surface is marked not-applicable in the project adapter.",
        )
    if command.lower() == "none":
        return ProbeResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            probe_outcome="skipped-explicit-none",
            exit_code="n/a",
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            evidence_summary="Surface is explicitly set to none.",
        )
    if entry.status == "known-broken" and not include_known_broken:
        return ProbeResult(
            surface=entry.surface,
            scope=entry.scope,
            declared_status=entry.status,
            probe_outcome="skipped-known-broken",
            exit_code="n/a",
            command_or_source=command,
            fallback_or_stop=entry.fallback_or_stop,
            evidence_summary="Known-broken surfaces are skipped unless explicitly included.",
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
    return ProbeResult(
        surface=entry.surface,
        scope=entry.scope,
        declared_status=entry.status,
        probe_outcome="success" if completed.returncode == 0 else "failure",
        exit_code=str(completed.returncode),
        command_or_source=command,
        fallback_or_stop=entry.fallback_or_stop,
        evidence_summary=_summarize_output(completed),
    )


def _render_receipt(
    template: str,
    *,
    receipt_id: str,
    generated_at: str,
    repository_root: Path,
    probe_mode: str,
    selected_surfaces: list[str],
    result_rows: str,
) -> str:
    rendered = template
    replacements = {
        "[receipt-id]": receipt_id,
        "[generated-at]": generated_at,
        "[repository-root]": str(repository_root),
        "[.github/instructions/project-context.instructions.md]": ".github/instructions/project-context.instructions.md",
        "[single-surface | all-surfaces]": probe_mode,
        "[selected-surfaces]": ", ".join(selected_surfaces) if selected_surfaces else "all declared surfaces",
        "| [surface] | [scope] | [declared status] | [success | failure | skipped-known-broken | skipped-explicit-none | not-applicable] | [exit code or `n/a`] | [command] | [fallback or stop] | [short summary] |": result_rows,
    }
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Developer Toolchain surfaces")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to probe")
    parser.add_argument(
        "--surface",
        action="append",
        default=[],
        help="Exact surface label or base surface kind to probe; may be repeated",
    )
    parser.add_argument(
        "--include-known-broken",
        action="store_true",
        help="Probe known-broken surfaces instead of skipping them",
    )
    parser.add_argument("--timeout", type=int, default=120, help="Per-command timeout in seconds")
    parser.add_argument("--receipt-id", help="Override the generated receipt id")
    parser.add_argument("--output", type=Path, help="Override receipt output path")
    args = parser.parse_args()

    root = args.root.resolve()
    project_context = root / ".github" / "instructions" / "project-context.instructions.md"
    if not project_context.is_file():
        raise SystemExit("project context file is missing")

    text = project_context.read_text(encoding="utf-8")
    _, _, entries = parse_developer_toolchain_entries(text)
    if not entries:
        raise SystemExit("Developer Toolchain section has no structured entries")

    selected_entries = _select_entries(entries, args.surface)
    receipt_id = args.receipt_id or _build_receipt_id()
    output_path = _resolve_output(root, args.output, receipt_id)

    results = [
        _probe_entry(
            entry,
            root=root,
            timeout=args.timeout,
            include_known_broken=args.include_known_broken,
        )
        for entry in selected_entries
    ]

    result_rows = "\n".join(
        f"| {result.surface} | {result.scope} | {result.declared_status} | {result.probe_outcome} | {result.exit_code} | {result.command_or_source} | {result.fallback_or_stop} | {result.evidence_summary} |"
        for result in results
    )

    template = (root / "templates" / "developer_toolchain_probe_receipt.template.md").read_text(encoding="utf-8")
    rendered = _render_receipt(
        template,
        receipt_id=receipt_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        repository_root=root,
        probe_mode="single-surface" if args.surface else "all-surfaces",
        selected_surfaces=[entry.surface for entry in selected_entries],
        result_rows=result_rows,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
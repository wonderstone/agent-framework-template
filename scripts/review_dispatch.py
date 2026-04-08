#!/usr/bin/env python3
"""Probe and dispatch local executor reviews using a machine-local registry."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY_PATH = ".github/local_executor_registry.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "tmp" / "executor_reviews"


@dataclass(frozen=True)
class ExecutorEntry:
    name: str
    probe_command: str
    review_command: str


@dataclass(frozen=True)
class ExecutorResult:
    name: str
    probe_status: str
    review_status: str
    stdout_path: str
    stderr_path: str
    notes: str


def _build_review_id() -> str:
    return datetime.now(timezone.utc).strftime("executor-review-%Y%m%dT%H%M%SZ")


def _load_registry(path: Path) -> list[ExecutorEntry]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise SystemExit("unsupported executor registry schema_version")
    executors = payload.get("executors")
    if not isinstance(executors, list) or not executors:
        raise SystemExit("executor registry has no executors")
    entries: list[ExecutorEntry] = []
    for raw in executors:
        if not isinstance(raw, dict):
            raise SystemExit("executor entry must be an object")
        try:
            name = str(raw["name"]).strip()
            probe_command = str(raw["probe_command"]).strip()
            review_command = str(raw["review_command"]).strip()
        except KeyError as exc:
            raise SystemExit(f"executor entry is missing key: {exc.args[0]}") from exc
        if not name or not probe_command or not review_command:
            raise SystemExit("executor entry fields must be non-empty")
        entries.append(ExecutorEntry(name=name, probe_command=probe_command, review_command=review_command))
    return entries


def _render_packet(template: str, *, generated_at: str, review_id: str, repository_root: Path, registry_path: Path, prompt_file: str, result_rows: str) -> str:
    rendered = template
    replacements = {
        "[generated-at]": generated_at,
        "[review-id]": review_id,
        "[repository-root]": str(repository_root),
        "[registry-path]": str(registry_path),
        "[prompt-file]": prompt_file,
        "| [executor] | [available | unavailable] | [completed | unavailable | dispatch-failed | skipped] | [stdout-path or `none`] | [stderr-path or `none`] | [notes] |": result_rows,
    }
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered.rstrip() + "\n"


def _probe_executor(entry: ExecutorEntry, root: Path) -> tuple[str, str]:
    completed = subprocess.run(
        entry.probe_command,
        cwd=root,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return "available", "Probe command succeeded."
    stderr = (completed.stderr or completed.stdout or "probe command failed").strip().splitlines()
    note = stderr[0].strip() if stderr else "probe command failed"
    return "unavailable", note[:240]


def _dispatch_executor(entry: ExecutorEntry, *, root: Path, prompt_file: Path, output_dir: Path) -> tuple[str, str, str]:
    stdout_path = output_dir / f"{entry.name}.stdout"
    stderr_path = output_dir / f"{entry.name}.stderr"
    command = entry.review_command.format(repo_root=str(root), prompt_file=str(prompt_file))
    completed = subprocess.run(
        command,
        cwd=root,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout_path.write_text(completed.stdout or "", encoding="utf-8")
    stderr_path.write_text(completed.stderr or "", encoding="utf-8")
    if completed.returncode == 0:
        return "completed", str(stdout_path), str(stderr_path)
    return "dispatch-failed", str(stdout_path), str(stderr_path)


def _write_packet(root: Path, *, review_id: str, registry_path: Path, prompt_file: str, results: list[ExecutorResult], output_root: Path) -> Path:
    output_dir = output_root / review_id
    packet_path = output_dir / "review_dispatch_packet.md"
    template = (root / "templates" / "review_dispatch_packet.template.md").read_text(encoding="utf-8")
    rows = "\n".join(
        f"| {result.name} | {result.probe_status} | {result.review_status} | {result.stdout_path} | {result.stderr_path} | {result.notes} |"
        for result in results
    )
    rendered = _render_packet(
        template,
        generated_at=datetime.now(timezone.utc).isoformat(),
        review_id=review_id,
        repository_root=root,
        registry_path=registry_path,
        prompt_file=prompt_file,
        result_rows=rows,
    )
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(rendered, encoding="utf-8")
    return packet_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe and dispatch local executor reviews")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--review-id")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("probe", help="Probe executor availability and write a packet")

    dispatch_parser = subparsers.add_parser("dispatch", help="Dispatch review commands and write a packet")
    dispatch_parser.add_argument("--prompt-file", type=Path, required=True)

    args = parser.parse_args()
    root = args.root.resolve()
    registry_path = (root / args.registry).resolve()
    if not registry_path.is_file():
        raise SystemExit("executor registry file is missing")
    entries = _load_registry(registry_path)
    review_id = args.review_id or _build_review_id()
    raw_output_dir = args.output_root / review_id / "raw"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    results: list[ExecutorResult] = []
    prompt_display = "none"
    prompt_file = None
    if args.command == "dispatch":
        prompt_file = args.prompt_file.resolve()
        if not prompt_file.is_file():
            raise SystemExit("prompt file is missing")
        prompt_display = str(prompt_file)

    for entry in entries:
        probe_status, probe_note = _probe_executor(entry, root)
        if probe_status != "available":
            results.append(
                ExecutorResult(
                    name=entry.name,
                    probe_status=probe_status,
                    review_status="unavailable" if args.command == "dispatch" else "skipped",
                    stdout_path="none",
                    stderr_path="none",
                    notes=probe_note,
                )
            )
            continue

        if args.command == "probe":
            results.append(
                ExecutorResult(
                    name=entry.name,
                    probe_status="available",
                    review_status="skipped",
                    stdout_path="none",
                    stderr_path="none",
                    notes="Probe command succeeded.",
                )
            )
            continue

        assert prompt_file is not None
        review_status, stdout_path, stderr_path = _dispatch_executor(
            entry,
            root=root,
            prompt_file=prompt_file,
            output_dir=raw_output_dir,
        )
        notes = "Review command completed." if review_status == "completed" else "Review command failed."
        results.append(
            ExecutorResult(
                name=entry.name,
                probe_status="available",
                review_status=review_status,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                notes=notes,
            )
        )

    packet_path = _write_packet(
        root,
        review_id=review_id,
        registry_path=registry_path,
        prompt_file=prompt_display,
        results=results,
        output_root=args.output_root,
    )
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
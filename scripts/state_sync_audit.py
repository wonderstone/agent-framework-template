#!/usr/bin/env python3
"""Audit execution-state sync across task artifacts, session state, and roadmap surfaces."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = "tmp/git_audit"
PROGRESS_RECEIPT_PATTERN = re.compile(rf"^{TASK_ROOT}/[^/]+/progress_receipts/[^/]+\.md$")
TASK_ARTIFACT_PATTERN = re.compile(rf"^{TASK_ROOT}/[^/]+/(?:audit_receipt|handoff_packet|task_packet|drift_packet)\.md$")


@dataclass(frozen=True)
class StateSyncIssue:
    kind: str
    detail: str


@dataclass(frozen=True)
class DiffLine:
    path: str
    content: str


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "state_sync_task"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_field(text: str, label: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(label)}\*\*:\s*(.+)$", text, flags=re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip()


def _extract_packet_field(text: str, label: str) -> str | None:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", text, flags=re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip()


def _extract_markdown_section(text: str, heading: str) -> str | None:
    heading_match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if heading_match is None:
        return None
    start = heading_match.end()
    next_heading = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    if next_heading is None:
        return text[start:]
    return text[start : start + next_heading.start()]


def _normalize_value(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value.strip().lower())


def _is_none_like(value: str | None) -> bool:
    normalized = _normalize_value(value)
    return (
        normalized in {"", "none", "(none)", "n/a"}
        or normalized.startswith("no active")
        or normalized.startswith("[")
        or "none]" in normalized
    )


def _is_no_active_work(value: str | None) -> bool:
    normalized = _normalize_value(value)
    return normalized.startswith("no active") or normalized == "idle"


def _load_progress_receipts(task_dir: Path) -> list[Path]:
    receipts_dir = task_dir / "progress_receipts"
    if not receipts_dir.is_dir():
        return []
    return sorted(receipts_dir.glob("*.md"))


def _latest_progress_status(task_dir: Path) -> str | None:
    receipts = _load_progress_receipts(task_dir)
    if not receipts:
        return None
    text = _read(receipts[-1])
    return _extract_packet_field(text, "Status")


def _drift_status(task_dir: Path) -> str | None:
    packet = task_dir / "drift_packet.md"
    if not packet.is_file():
        return None
    return _extract_packet_field(_read(packet), "Status")


def _has_open_drift(task_dir: Path) -> bool:
    status = _normalize_value(_drift_status(task_dir))
    return status in {"open", "in_progress", "in progress"}


def _find_leftover_reference(text: str, task_id: str) -> bool:
    leftovers = _extract_markdown_section(text, "Leftover Units") or ""
    return task_id in leftovers or _slugify(task_id) in leftovers


def audit_repo(root: Path) -> list[StateSyncIssue]:
    issues: list[StateSyncIssue] = []
    session_state_path = root / "session_state.md"
    if not session_state_path.is_file():
        return issues

    session_state = _read(session_state_path)
    active_task_id = _extract_field(session_state, "Active Task ID")
    current_step = _extract_field(session_state, "Current Step")
    blocker_section = (_extract_markdown_section(session_state, "Blocker / Decision Needed") or "").strip()

    for packet in sorted((root / TASK_ROOT).glob("*/drift_packet.md")):
        task_dir = packet.parent
        if _has_open_drift(task_dir):
            issues.append(
                StateSyncIssue(
                    "unresolved-drift-packet",
                    f"{packet.relative_to(root).as_posix()}: unresolved drift must be reconciled before closeout or next-stage dispatch",
                )
            )

    if _is_none_like(active_task_id):
        return issues

    task_dir = root / TASK_ROOT / _slugify(active_task_id or "")
    progress_receipts = _load_progress_receipts(task_dir)
    if not progress_receipts:
        issues.append(
            StateSyncIssue(
                "missing-progress-receipt",
                f"session_state.md: active task '{active_task_id}' has no progress receipt under {task_dir.relative_to(root).as_posix()}/progress_receipts/",
            )
        )

    latest_status = _normalize_value(_latest_progress_status(task_dir))
    handoff_exists = (task_dir / "handoff_packet.md").is_file()
    drift_open = _has_open_drift(task_dir)

    if _is_no_active_work(current_step) and (latest_status in {"blocked", "in_progress", "checkpoint_reached"} or handoff_exists):
        issues.append(
            StateSyncIssue(
                "stale-session-state-active-work",
                f"session_state.md: active task '{active_task_id}' is marked idle while receipts or handoff artifacts still show in-flight work",
            )
        )

    has_blocker = (
        blocker_section
        and blocker_section != "- (none)"
        and "[what is blocked]" not in blocker_section
    )
    if has_blocker and not handoff_exists and not _find_leftover_reference(session_state, active_task_id or "") and not drift_open:
        issues.append(
            StateSyncIssue(
                "blocker-without-recovery-artifact",
                f"session_state.md: active task '{active_task_id}' records a blocker without a matching handoff packet, leftover record, or open drift packet",
            )
        )

    return issues


def parse_added_lines(diff_text: str) -> list[DiffLine]:
    lines: list[DiffLine] = []
    current_path: str | None = None
    for raw_line in diff_text.splitlines():
        if raw_line.startswith("+++ b/"):
            current_path = raw_line[6:]
            continue
        if raw_line.startswith("+++ "):
            current_path = None
            continue
        if raw_line.startswith("diff --git ") or raw_line.startswith("@@"):
            continue
        if raw_line.startswith("+") and not raw_line.startswith("+++") and current_path:
            lines.append(DiffLine(path=current_path, content=raw_line[1:]))
    return lines


def audit_diff(diff_text: str) -> list[StateSyncIssue]:
    lines = parse_added_lines(diff_text)
    if not lines:
        return []

    changed_paths = {line.path for line in lines}
    issues: list[StateSyncIssue] = []
    has_progress_receipt = any(PROGRESS_RECEIPT_PATTERN.match(path) for path in changed_paths)
    has_task_artifact = any(TASK_ARTIFACT_PATTERN.match(path) for path in changed_paths)
    has_state_surface = "session_state.md" in changed_paths or "ROADMAP.md" in changed_paths
    has_drift_packet = any(path.endswith("/drift_packet.md") for path in changed_paths)
    has_handoff = any(path.endswith("/handoff_packet.md") for path in changed_paths)

    if has_progress_receipt and not (has_state_surface or has_drift_packet or has_handoff):
        issues.append(
            StateSyncIssue(
                "unsynced-progress-receipt",
                "progress receipt added without any matching session_state.md, ROADMAP.md, drift packet, or handoff update in the same diff",
            )
        )

    blocked_progress = any(
        PROGRESS_RECEIPT_PATTERN.match(line.path)
        and line.content.strip().lower() == "- status: blocked"
        for line in lines
    )
    if blocked_progress and not (has_handoff or has_drift_packet or "session_state.md" in changed_paths):
        issues.append(
            StateSyncIssue(
                "blocked-progress-without-recovery",
                "blocked progress receipt added without a handoff packet, drift packet, or session_state blocker update in the same diff",
            )
        )

    roadmap_completion = any(
        line.path == "ROADMAP.md" and "✅" in line.content for line in lines
    )
    if roadmap_completion and not (has_progress_receipt or has_task_artifact):
        issues.append(
            StateSyncIssue(
                "roadmap-completion-without-artifact",
                "ROADMAP.md completion was added without a matching progress receipt, audit receipt, handoff packet, task packet, or drift packet in the same diff",
            )
        )

    idle_transition = any(
        line.path == "session_state.md"
        and line.content.lower().startswith("**current step**: no active")
        for line in lines
    )
    if idle_transition and not (has_progress_receipt or has_task_artifact):
        issues.append(
            StateSyncIssue(
                "idle-state-without-artifact",
                "session_state.md was moved to no active work without a matching progress receipt, handoff packet, audit receipt, task packet, or drift packet in the same diff",
            )
        )

    return issues


def get_git_diff(root: Path, *, staged: bool) -> str:
    command = ["git", "-C", str(root), "diff", "--unified=0", "--no-color"]
    if staged:
        command.insert(4, "--cached")
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit execution-state sync surfaces")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root")
    parser.add_argument("--diff-file", type=Path, help="read diff from a file instead of git")
    parser.add_argument("--worktree", action="store_true", help="inspect unstaged diff instead of staged diff")
    parser.add_argument("--repo-only", action="store_true", help="skip diff checks and inspect repository state only")
    args = parser.parse_args()

    root = args.root.resolve()
    issues = audit_repo(root)

    if not args.repo_only:
        if args.diff_file:
            diff_text = args.diff_file.read_text(encoding="utf-8")
        else:
            diff_text = get_git_diff(root, staged=not args.worktree)
        issues.extend(audit_diff(diff_text))

    if not issues:
        print("state sync audit passed")
        return 0

    print("state sync audit failed")
    for issue in issues:
        print(f"- {issue.kind}: {issue.detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
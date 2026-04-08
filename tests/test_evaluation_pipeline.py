from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_evaluation_pipeline_creates_request_and_report(tmp_path: Path) -> None:
    request_output = tmp_path / "evaluation" / "task_1" / "evaluation_request.md"
    report_output = tmp_path / "evaluation" / "task_1" / "evaluation_report.md"
    script_path = REPO_ROOT / "scripts" / "evaluation_pipeline.py"

    request = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "init-request",
            "--task-id",
            "task-1",
            "--generator",
            "implementer",
            "--evaluator",
            "auditor",
            "--review-scope",
            "user-facing change",
            "--goal",
            "Confirm the generated output is acceptable.",
            "--uac-focus",
            "- [x] user sees the expected output",
            "--evidence-to-review",
            "- tests/test_example.py",
            "--allowed-files",
            "- src/example.py",
            "--do-not-touch",
            "- docs/archive/",
            "--output-root",
            str(tmp_path / "evaluation"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "record-report",
            "--task-id",
            "task-1",
            "--evaluator",
            "auditor",
            "--verdict",
            "PASS",
            "--uac-coverage",
            "- [x] output matched expectation",
            "--gap-check",
            "- no remaining user-visible gaps",
            "--evidence-anchors",
            "- pytest: 3 passed",
            "--output-root",
            str(tmp_path / "evaluation"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert request.stdout.strip() == str(request_output)
    assert report.stdout.strip() == str(report_output)
    assert "- Generator: implementer" in request_output.read_text(encoding="utf-8")
    assert "- Verdict: PASS" in report_output.read_text(encoding="utf-8")


def test_evaluation_pipeline_rejects_unknown_verdict(tmp_path: Path) -> None:
    script_path = REPO_ROOT / "scripts" / "evaluation_pipeline.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "record-report",
            "--task-id",
            "task-1",
            "--evaluator",
            "auditor",
            "--verdict",
            "MAYBE",
            "--uac-coverage",
            "- none",
            "--gap-check",
            "- none",
            "--evidence-anchors",
            "- none",
            "--output-root",
            str(tmp_path / "evaluation"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "unsupported verdict" in result.stderr
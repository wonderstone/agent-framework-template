#!/usr/bin/env python3
"""Generate independent evaluation request and report artifacts."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "tmp" / "evaluation"
ALLOWED_VERDICTS = {"PASS", "CONDITIONAL", "FAIL"}


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "evaluation_task"


def _normalize_block(value: str) -> str:
    text = value.strip()
    return text or "- none"


def _load_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def _render_template(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(key, value)
    return rendered.rstrip() + "\n"


def _task_dir(task_id: str, output_root: Path) -> Path:
    return output_root / _slugify(task_id)


@dataclass(frozen=True)
class RequestOptions:
    task_id: str
    generator: str
    evaluator: str
    review_scope: str
    goal: str
    uac_focus: str
    evidence_to_review: str
    allowed_files: str
    do_not_touch: str
    output_root: Path


@dataclass(frozen=True)
class ReportOptions:
    task_id: str
    evaluator: str
    verdict: str
    uac_coverage: str
    gap_check: str
    conditions: str
    blocking: str
    evidence_anchors: str
    output_root: Path


def create_request(options: RequestOptions) -> Path:
    template = _load_template("evaluation_request.template.md")
    output_path = _task_dir(options.task_id, options.output_root) / "evaluation_request.md"
    rendered = _render_template(
        template,
        {
            "[generated-at]": datetime.now(timezone.utc).isoformat(),
            "[task-id]": options.task_id,
            "[generator]": options.generator,
            "[evaluator]": options.evaluator,
            "[review-scope]": options.review_scope,
            "[goal]": options.goal,
            "[uac-focus]": _normalize_block(options.uac_focus),
            "[evidence-to-review]": _normalize_block(options.evidence_to_review),
            "[allowed-files]": _normalize_block(options.allowed_files),
            "[do-not-touch]": _normalize_block(options.do_not_touch),
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def create_report(options: ReportOptions) -> Path:
    if options.verdict not in ALLOWED_VERDICTS:
        raise SystemExit(f"unsupported verdict: {options.verdict}")
    template = _load_template("evaluation_report.template.md")
    output_path = _task_dir(options.task_id, options.output_root) / "evaluation_report.md"
    rendered = _render_template(
        template,
        {
            "[generated-at]": datetime.now(timezone.utc).isoformat(),
            "[task-id]": options.task_id,
            "[evaluator]": options.evaluator,
            "[PASS | CONDITIONAL | FAIL]": options.verdict,
            "[uac-coverage]": _normalize_block(options.uac_coverage),
            "[gap-check]": _normalize_block(options.gap_check),
            "[conditions]": _normalize_block(options.conditions),
            "[blocking]": _normalize_block(options.blocking),
            "[evidence-anchors]": _normalize_block(options.evidence_anchors),
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate independent evaluation artifacts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser("init-request", help="Create an evaluation request")
    request_parser.add_argument("--task-id", required=True)
    request_parser.add_argument("--generator", required=True)
    request_parser.add_argument("--evaluator", required=True)
    request_parser.add_argument("--review-scope", required=True)
    request_parser.add_argument("--goal", required=True)
    request_parser.add_argument("--uac-focus", required=True)
    request_parser.add_argument("--evidence-to-review", required=True)
    request_parser.add_argument("--allowed-files", required=True)
    request_parser.add_argument("--do-not-touch", required=True)
    request_parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    report_parser = subparsers.add_parser("record-report", help="Create an evaluation report")
    report_parser.add_argument("--task-id", required=True)
    report_parser.add_argument("--evaluator", required=True)
    report_parser.add_argument("--verdict", required=True)
    report_parser.add_argument("--uac-coverage", required=True)
    report_parser.add_argument("--gap-check", required=True)
    report_parser.add_argument("--conditions", default="- none")
    report_parser.add_argument("--blocking", default="- none")
    report_parser.add_argument("--evidence-anchors", required=True)
    report_parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    args = parser.parse_args()
    if args.command == "init-request":
        output_path = create_request(
            RequestOptions(
                task_id=args.task_id,
                generator=args.generator,
                evaluator=args.evaluator,
                review_scope=args.review_scope,
                goal=args.goal,
                uac_focus=args.uac_focus,
                evidence_to_review=args.evidence_to_review,
                allowed_files=args.allowed_files,
                do_not_touch=args.do_not_touch,
                output_root=args.output_root,
            )
        )
    else:
        output_path = create_report(
            ReportOptions(
                task_id=args.task_id,
                evaluator=args.evaluator,
                verdict=args.verdict,
                uac_coverage=args.uac_coverage,
                gap_check=args.gap_check,
                conditions=args.conditions,
                blocking=args.blocking,
                evidence_anchors=args.evidence_anchors,
                output_root=args.output_root,
            )
        )

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
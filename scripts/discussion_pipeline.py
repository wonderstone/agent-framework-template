#!/usr/bin/env python3
"""Generate and extend multi-model discussion packet assets."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "tmp" / "discussion"


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "discussion_topic"


def _normalize_block(value: str) -> str:
    text = value.strip()
    return text or "- none"


def render_template(template_text: str, values: dict[str, str]) -> str:
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_topic_dir(topic_id: str, output_root: Path) -> Path:
    return output_root / _slugify(topic_id)


def load_template(template_name: str) -> str:
    return (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")


def write_rendered_file(output_path: Path, contents: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(contents.rstrip() + "\n", encoding="utf-8")
    return output_path


def append_to_file(output_path: Path, contents: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not output_path.exists():
        raise FileNotFoundError(output_path)
    existing = output_path.read_text(encoding="utf-8").rstrip()
    output_path.write_text(existing + "\n\n" + contents.rstrip() + "\n", encoding="utf-8")
    return output_path


@dataclass(frozen=True)
class DiscussionPacketOptions:
    topic_id: str
    decision_question: str
    why_now: str
    current_truth: str
    constraints: str
    candidate_directions: str
    evaluation_criteria: str
    suggested_executors: str
    round_goal: str
    round_exit_rule: str
    owner: str
    output_root: Path


@dataclass(frozen=True)
class FeedbackOptions:
    topic_id: str
    round_name: str
    executor: str
    stance: str
    summary: str
    strengths: str
    risks: str
    open_questions: str
    recommended_next_step: str
    output_root: Path


@dataclass(frozen=True)
class SynthesisOptions:
    topic_id: str
    round_name: str
    decision: str
    confidence: str
    summary: str
    rationale: str
    next_action: str
    follow_up_questions: str
    output_root: Path


def create_discussion_packet(options: DiscussionPacketOptions) -> Path:
    template = load_template("discussion_packet.template.md")
    output_path = build_topic_dir(options.topic_id, options.output_root) / "discussion_packet.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "topic_id": options.topic_id,
            "owner": options.owner,
            "round_goal": options.round_goal,
            "round_exit_rule": options.round_exit_rule,
            "decision_question": options.decision_question,
            "why_now": _normalize_block(options.why_now),
            "current_truth": _normalize_block(options.current_truth),
            "constraints": _normalize_block(options.constraints),
            "candidate_directions": _normalize_block(options.candidate_directions),
            "evaluation_criteria": _normalize_block(options.evaluation_criteria),
            "suggested_executors": _normalize_block(options.suggested_executors),
        },
    )
    return write_rendered_file(output_path, contents)


def append_feedback(options: FeedbackOptions) -> Path:
    output_path = build_topic_dir(options.topic_id, options.output_root) / "discussion_packet.md"
    block = render_template(
        """
---

## Feedback — {{round_name}} — {{executor}}

- Timestamp: {{generated_at}}
- Stance: {{stance}}
- Summary: {{summary}}

### Strengths

{{strengths}}

### Risks

{{risks}}

### Open Questions

{{open_questions}}

### Recommended Next Step

{{recommended_next_step}}
""".strip(),
        {
            "round_name": options.round_name,
            "executor": options.executor,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stance": options.stance,
            "summary": options.summary,
            "strengths": _normalize_block(options.strengths),
            "risks": _normalize_block(options.risks),
            "open_questions": _normalize_block(options.open_questions),
            "recommended_next_step": _normalize_block(options.recommended_next_step),
        },
    )
    return append_to_file(output_path, block)


def append_synthesis(options: SynthesisOptions) -> Path:
    output_path = build_topic_dir(options.topic_id, options.output_root) / "discussion_packet.md"
    block = render_template(
        """
---

## Main-Thread Synthesis — {{round_name}}

- Timestamp: {{generated_at}}
- Decision: {{decision}}
- Confidence: {{confidence}}
- Next action: {{next_action}}

### Summary

{{summary}}

### Rationale

{{rationale}}

### Follow-Up Questions

{{follow_up_questions}}
""".strip(),
        {
            "round_name": options.round_name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "decision": options.decision,
            "confidence": options.confidence,
            "next_action": options.next_action,
            "summary": _normalize_block(options.summary),
            "rationale": _normalize_block(options.rationale),
            "follow_up_questions": _normalize_block(options.follow_up_questions),
        },
    )
    return append_to_file(output_path, block)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and extend multi-model discussion packet assets"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_topic = subparsers.add_parser("init-topic", help="Create a discussion packet")
    init_topic.add_argument("--topic-id", required=True)
    init_topic.add_argument("--decision-question", required=True)
    init_topic.add_argument("--why-now", required=True)
    init_topic.add_argument("--current-truth", required=True)
    init_topic.add_argument("--constraints", required=True)
    init_topic.add_argument("--candidate-directions", required=True)
    init_topic.add_argument("--evaluation-criteria", required=True)
    init_topic.add_argument("--suggested-executors", required=True)
    init_topic.add_argument("--round-goal", default="Obtain enough judgment to freeze a plan")
    init_topic.add_argument(
        "--round-exit-rule",
        default="Freeze a plan, narrow to a sharper second round, or stop on missing truth",
    )
    init_topic.add_argument("--owner", default="main-thread")
    init_topic.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    append_feedback_parser = subparsers.add_parser(
        "append-feedback", help="Append one executor feedback block"
    )
    append_feedback_parser.add_argument("--topic-id", required=True)
    append_feedback_parser.add_argument("--round-name", default="Round 1")
    append_feedback_parser.add_argument("--executor", required=True)
    append_feedback_parser.add_argument("--stance", required=True)
    append_feedback_parser.add_argument("--summary", required=True)
    append_feedback_parser.add_argument("--strengths", required=True)
    append_feedback_parser.add_argument("--risks", required=True)
    append_feedback_parser.add_argument("--open-questions", default="- none")
    append_feedback_parser.add_argument("--recommended-next-step", default="- none")
    append_feedback_parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    append_synthesis_parser = subparsers.add_parser(
        "append-synthesis", help="Append the main-thread synthesis block"
    )
    append_synthesis_parser.add_argument("--topic-id", required=True)
    append_synthesis_parser.add_argument("--round-name", default="Round 1")
    append_synthesis_parser.add_argument(
        "--decision",
        required=True,
        help="Typical values: freeze-plan, continue-discussion, stop",
    )
    append_synthesis_parser.add_argument("--confidence", required=True)
    append_synthesis_parser.add_argument("--summary", required=True)
    append_synthesis_parser.add_argument("--rationale", required=True)
    append_synthesis_parser.add_argument("--next-action", required=True)
    append_synthesis_parser.add_argument("--follow-up-questions", default="- none")
    append_synthesis_parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "init-topic":
        output_path = create_discussion_packet(
            DiscussionPacketOptions(
                topic_id=args.topic_id,
                decision_question=args.decision_question,
                why_now=args.why_now,
                current_truth=args.current_truth,
                constraints=args.constraints,
                candidate_directions=args.candidate_directions,
                evaluation_criteria=args.evaluation_criteria,
                suggested_executors=args.suggested_executors,
                round_goal=args.round_goal,
                round_exit_rule=args.round_exit_rule,
                owner=args.owner,
                output_root=args.output_root,
            )
        )
    elif args.command == "append-feedback":
        output_path = append_feedback(
            FeedbackOptions(
                topic_id=args.topic_id,
                round_name=args.round_name,
                executor=args.executor,
                stance=args.stance,
                summary=args.summary,
                strengths=args.strengths,
                risks=args.risks,
                open_questions=args.open_questions,
                recommended_next_step=args.recommended_next_step,
                output_root=args.output_root,
            )
        )
    else:
        output_path = append_synthesis(
            SynthesisOptions(
                topic_id=args.topic_id,
                round_name=args.round_name,
                decision=args.decision,
                confidence=args.confidence,
                summary=args.summary,
                rationale=args.rationale,
                next_action=args.next_action,
                follow_up_questions=args.follow_up_questions,
                output_root=args.output_root,
            )
        )

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

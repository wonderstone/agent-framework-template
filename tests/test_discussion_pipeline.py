from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "discussion_pipeline.py"
SPEC = importlib.util.spec_from_file_location("discussion_pipeline", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

DiscussionPacketOptions = MODULE.DiscussionPacketOptions
FeedbackOptions = MODULE.FeedbackOptions
SynthesisOptions = MODULE.SynthesisOptions
append_feedback = MODULE.append_feedback
append_synthesis = MODULE.append_synthesis
build_topic_dir = MODULE.build_topic_dir
create_discussion_packet = MODULE.create_discussion_packet
render_template = MODULE.render_template


def test_render_template_replaces_known_placeholders() -> None:
    template = "Decision {{topic_id}} owned by {{owner}}"

    rendered = render_template(template, {"topic_id": "routing-review", "owner": "main-thread"})

    assert rendered == "Decision routing-review owned by main-thread"


def test_create_discussion_packet_writes_markdown_from_template(tmp_path: Path) -> None:
    output_path = create_discussion_packet(
        DiscussionPacketOptions(
            topic_id="Routing Review",
            decision_question="Which routing strategy should we adopt?",
            why_now="- We need to freeze the framework before implementation.",
            current_truth="- Existing code is still flexible.",
            constraints="- Minimize migration risk.",
            candidate_directions="- Option A\n- Option B",
            evaluation_criteria="- Runtime safety\n- Implementation cost",
            suggested_executors="- claude-code\n- codex\n- internal-subagent",
            round_goal="Pick one direction or narrow to two finalists",
            round_exit_rule="Freeze a plan or start a sharper second round",
            owner="main-thread",
            output_root=tmp_path,
        )
    )

    assert output_path == build_topic_dir("Routing Review", tmp_path) / "discussion_packet.md"
    contents = output_path.read_text(encoding="utf-8")
    assert "Which routing strategy should we adopt?" in contents
    assert "claude-code" in contents


def test_append_feedback_adds_executor_block_to_packet(tmp_path: Path) -> None:
    create_discussion_packet(
        DiscussionPacketOptions(
            topic_id="Routing Review",
            decision_question="Which routing strategy should we adopt?",
            why_now="- Decision needed before code changes.",
            current_truth="- Current implementation is not frozen.",
            constraints="- Keep rollback simple.",
            candidate_directions="- Option A\n- Option B",
            evaluation_criteria="- Complexity\n- Compatibility",
            suggested_executors="- codex",
            round_goal="Collect first-pass opinions",
            round_exit_rule="Freeze or narrow",
            owner="main-thread",
            output_root=tmp_path,
        )
    )

    output_path = append_feedback(
        FeedbackOptions(
            topic_id="Routing Review",
            round_name="Round 1",
            executor="codex",
            stance="prefer option A",
            summary="Option A reduces migration surface.",
            strengths="- Smaller diff",
            risks="- Slightly less flexible later",
            open_questions="- Does the team need pluggable backends now?",
            recommended_next_step="- Ask one more reviewer to compare extensibility needs.",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "## Feedback — Round 1 — codex" in contents
    assert "Option A reduces migration surface." in contents


def test_append_synthesis_records_main_thread_decision(tmp_path: Path) -> None:
    create_discussion_packet(
        DiscussionPacketOptions(
            topic_id="Routing Review",
            decision_question="Which routing strategy should we adopt?",
            why_now="- Decision needed before code changes.",
            current_truth="- Current implementation is not frozen.",
            constraints="- Keep rollback simple.",
            candidate_directions="- Option A\n- Option B",
            evaluation_criteria="- Complexity\n- Compatibility",
            suggested_executors="- codex",
            round_goal="Collect first-pass opinions",
            round_exit_rule="Freeze or narrow",
            owner="main-thread",
            output_root=tmp_path,
        )
    )

    output_path = append_synthesis(
        SynthesisOptions(
            topic_id="Routing Review",
            round_name="Round 1",
            decision="freeze-plan",
            confidence="medium",
            summary="Option A is the best conservative default.",
            rationale="- It wins on migration safety and keeps future extension open enough.",
            next_action="Promote Option A into the execution checklist before coding.",
            follow_up_questions="- none",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "## Main-Thread Synthesis — Round 1" in contents
    assert "freeze-plan" in contents
    assert "Promote Option A into the execution checklist before coding." in contents

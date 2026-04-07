from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "skill_evolution_pipeline.py"
SPEC = importlib.util.spec_from_file_location("skill_evolution_pipeline", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

CandidatePacketOptions = MODULE.CandidatePacketOptions
InvocationReceiptOptions = MODULE.InvocationReceiptOptions
create_candidate_packet = MODULE.create_candidate_packet
create_invocation_receipt = MODULE.create_invocation_receipt


def test_create_invocation_receipt_renders_runtime_evidence(tmp_path: Path) -> None:
    output_path = tmp_path / "invocation.md"

    create_invocation_receipt(
        InvocationReceiptOptions(
            receipt_id="receipt-1",
            invocation_id="invoke-1",
            skill_id="discussion-packet-first",
            trigger_class="explicit-request",
            execution_mode="local-follow",
            outcome="success",
            candidate_recommendation="CAPTURED",
            trigger_reason="- The task explicitly required the discussion workflow.",
            references_loaded="| discussion runbook | docs/runbooks/multi-model-discussion-loop.md | yes | Needed to follow the canonical round loop |",
            outcome_summary="- The packet was created and four CLI outputs were gathered successfully.",
            evidence_links="| packet-1 | task artifact | Proves the workflow ran against a durable packet |",
            follow_up_recommendation="- Recommend CAPTURED because the execution sequence is now a reusable runtime pattern.",
            output_path=output_path,
        )
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "- Receipt ID: receipt-1" in rendered
    assert "- Invocation ID: invoke-1" in rendered
    assert "- Candidate Recommendation: CAPTURED" in rendered
    assert "discussion runbook" in rendered
    assert "packet-1" in rendered


def test_create_candidate_packet_renders_lineage_fields(tmp_path: Path) -> None:
    output_path = tmp_path / "candidate.md"

    create_candidate_packet(
        CandidatePacketOptions(
            candidate_id="candidate-1",
            source_skill="discussion-packet-first",
            harvest_source="invocation receipt",
            proposed_by="skill-harvester",
            confidence_tier="medium",
            evolution_mode="DERIVED",
            candidate_trigger="repeated-successful-reuse",
            invocation_ids="invoke-1, invoke-2",
            parent_lineage="discussion-packet-first",
            target_fields="- entry_instructions\n- references",
            proposed_delta="- Add a stronger execution-side packet append pattern for long-running multi-CLI rounds.",
            evidence_bundle="| receipt-1 | invocation | Shows the runtime pattern worked across multiple rounds |",
            escalation_triggers="- Escalate if the candidate tries to widen trigger scope.",
            notes="- Keep canonical mutation behind the existing promotion path.",
            output_path=output_path,
        )
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "- Candidate ID: candidate-1" in rendered
    assert "- Evolution Mode: DERIVED" in rendered
    assert "- Candidate Trigger: repeated-successful-reuse" in rendered
    assert "- Invocation IDs: invoke-1, invoke-2" in rendered
    assert "- Parent Lineage: discussion-packet-first" in rendered
    assert "receipt-1" in rendered
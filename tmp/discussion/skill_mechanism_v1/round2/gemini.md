## Verdict
Support the hybrid direction: a framework-native SKILL contract serves as the truthful, executable core, while vendor-specific formats and package distribution remain optional, generated adapter layers.

## Canonical V1 Contract
The framework-native SKILL contract must be minimal but executable. It should include the following sections:
- **Type Declaration:** Explicitly classify the skill (e.g., Knowledge, Workflow, Guardrail, Verification) to determine its baseline execution rules.
- **Trigger Semantics:** A concise, intent-based description defining exactly when the skill should be invoked and, crucially, when it must be ignored.
- **Progressive Disclosure Pointers:** File paths to supporting documentation, executable scripts, and deeper context, ensuring the top-level contract remains lean.
- **Execution Invariants:** Hard constraints or prerequisites (e.g., required environment variables, setup commands) that must be verified before proceeding.
- **Gotchas / Anti-Patterns:** A living list of hard-won lessons, edge cases, and known failures to prevent repetitive regressions.
- **Evidence Ledger Link:** A pointer to the audit trail, receipts, or pull requests that justify the current state of the skill.

## Evidence And Update Gates
To prevent silent prompt drift, skill updates must be strictly governed based on the quality of the underlying evidence.
- **Rank 1 (Authoritative):** CI/CD pipeline failures, validator rejections, and empirically proven runtime execution errors.
- **Rank 2 (Strong):** Explicit human review feedback, architectural decisions, and closeout summaries from completed tasks.
- **Rank 3 (Advisory):** Agent-generated execution receipts and self-reported gotchas discovered during a session.

**Gates:** Rank 1 and Rank 3 evidence may be auto-collected into a "proposed updates" ledger (e.g., a candidate PR or a pending discussion packet). However, *all* modifications to the canonical SKILL contract must require explicit human review and approval. Auto-committing changes to a skill's behavior based purely on agent self-reflection is forbidden, as it guarantees unchecked, silent drift over time.

## Trigger And Validation Contract
- **Minimum Triggerability Contract:** The skill must expose a short, unambiguous condition (e.g., "Use this when modifying authentication logic") that any agent can evaluate within its default context window without loading the full payload.
- **Active Validation:** Validators must strictly enforce that pointers to supporting files resolve correctly, that execution invariants (like the presence of required CLI tools) are structurally verifiable, and that the type declaration is valid.
- **Advisory Validation:** The formatting of gotchas and the stylistic phrasing of the trigger condition should remain advisory, to be refined by human reviewers.
- **Progressive Disclosure Truthfulness:** Validators must ensure that supporting files do not contradict the top-level invariants. The entry point must remain a strict index, preventing it from ballooning into a monolithic guide.

## Portability And Honest Degradation
- **Core and Portable:** The type declaration, trigger semantics, invariants, and gotchas are universal concepts. They can be parsed and translated into any agent's default prompt or context format.
- **Optional Adapters:** Complex execution hooks, vendor-specific syntax (like custom XML tags or proprietary tool calls), and automated subagent delegation must be modeled as optional adapters.
- **Honest Degradation:** If a specific agent does not support hooks or multi-step subagent delegation, the framework must gracefully degrade. It should fall back to presenting the skill's invariants and scripts as read-only, manual instructions (e.g., "Run this validation script manually in the terminal and verify the output before proceeding").

## Biggest Risk
The single highest-risk failure mode is "Skill Bloat." If the mechanism allows the contract to become a monolithic, overly complex repository of taxonomy, agents will either ignore it because the context cost is too high or fail to trigger it reliably because the entry conditions are buried under paragraphs of prose.

## Narrowest Next Question
What is the exact schema and lifecycle for a "Skill Update Receipt" to ensure that gathered gotchas and execution failures are structured enough for a human to review quickly without having to parse raw session logs?
lently.

## Biggest Risk
The single highest-risk failure mode is "Trigger Bloat," where trigger conditions become so broad, ambiguous, and overlapping that the agent loads multiple conflicting skills into context on every turn, instantly collapsing the progressive disclosure model and destroying context efficiency.

## Narrowest Next Question
How do we mechanically enforce mutually exclusive or strictly hierarchical trigger conditions across multiple skills to prevent overlapping context bloat without requiring a centralized human arbiter?

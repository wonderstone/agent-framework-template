# Task Packet — Runtime Alignment Adoption Guide Follow-up

## Task ID
`runtime-alignment-adoption-guide-followup`

## Goal
Update `docs/ADOPTION_GUIDE.md` so adopters can discover and keep the runtime-alignment asset family without relying on maintainer-only state or roadmap context.

## Why This Slice Exists
The runtime-alignment and four-lane delegation asset family is already shipped mechanically:
- `docs/runbooks/runtime_alignment_and_four_lane_delegation.md`
- `templates/four_lane_runtime_alignment_status.template.md`

Those assets are already wired into bootstrap, validator, README, docs index, and project-context routing.

The remaining gap is adopter-facing discoverability:
- `docs/ADOPTION_GUIDE.md` still does not mention this asset family in the manual-adoption inventory.
- `docs/ADOPTION_GUIDE.md` still does not explain when adopters should keep these surfaces.

## Authorized Scope
Edit only:
- `docs/ADOPTION_GUIDE.md`

You may read for consistency:
- `README.md`
- `docs/INDEX.md`
- `docs/runbooks/runtime_alignment_and_four_lane_delegation.md`
- `templates/four_lane_runtime_alignment_status.template.md`
- `.github/instructions/project-context.instructions.md`
- `ROADMAP.md`
- `session_state.md`

## Do Not Touch
Do not edit:
- `scripts/bootstrap_adoption.py`
- `scripts/validate_template.py`
- `tests/`
- `.github/copilot-instructions.md`
- `.github/instructions/project-context.instructions.md`
- `README.md`
- `docs/INDEX.md`
- `ROADMAP.md`
- `session_state.md`

## User Acceptance Criteria
- [ ] Manual adopters can see `docs/runbooks/runtime_alignment_and_four_lane_delegation.md` in the file inventory where it naturally belongs.
- [ ] Manual adopters can see `templates/four_lane_runtime_alignment_status.template.md` in the template inventory where it naturally belongs.
- [ ] The guide explicitly explains when adopters should keep these surfaces, for example when they care about repo-target vs running-runtime alignment, runtime-dependent acceptance, or honest multi-lane status reporting.
- [ ] The wording stays generic to the template repo and does not leak QuantOS-specific implementation details.
- [ ] The edit is minimal and does not reopen bootstrap, validator, or unrelated frontend-diagnostics work.

## Start Here
1. Read `docs/ADOPTION_GUIDE.md`.
2. Read the new runbook and template to confirm their exact names and purpose.
3. Add the runbook and template to the relevant manual-copy lists.
4. Add one short guidance paragraph or bullet group explaining when adopters should keep the runtime-alignment and four-lane status surfaces.
5. Keep the patch small and consistent with existing guide style.

## Focused Validation
Run the narrowest honest validation available for this docs-only slice:
- `python3 scripts/active_docs_audit.py`

If that check fails for unrelated pre-existing reasons, record that explicitly in the receipt instead of widening scope.

## Deliverable
When finished, report:
1. what changed in `docs/ADOPTION_GUIDE.md`
2. whether `python3 scripts/active_docs_audit.py` passed or failed
3. any residual risk or wording ambiguity
4. a short receipt in `tmp/git_audit/runtime_alignment_adoption_guide_followup/audit_receipt.md`

## Output Contract
End in exactly one of:
- `DONE`
- `STUCK`
- `ESCALATE`

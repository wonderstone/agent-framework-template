# Adoption Guide

Step-by-step guide for adopting this agent framework in a new project.

---

## Prerequisites

- GitHub repository (new or existing)
- A coding assistant that reads `.github/copilot-instructions.md` (GitHub Copilot, Cursor, Augment, etc.)
- Bash (to run `scripts/validate-template.sh` after setup)

---

## Step 1 — Copy the Core Files

Copy these files into your new repository, preserving their paths:

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–11)
  project-context.instructions.md  ← project adapter (fill in Step 2)
  agents/
    architect.agent.md             ← analysis/planning agent
    implementer.agent.md           ← execution/validation agent
  instructions/
    backend.instructions.md        ← backend change protocol
    docs.instructions.md           ← documentation change protocol

docs/
  INDEX.md                         ← TYPE-A doc navigation index
  FRAMEWORK_ARCHITECTURE.md        ← how the layers work (optional, keep for ref)
  ADOPTION_GUIDE.md                ← this file (optional, keep for ref)
  STRATEGY_MECHANISM_LAYERING.md   ← keep if you want formal reviewer or agent role splits
  ROLE_STRATEGY_EXAMPLES.md        ← keep if you want ready-to-adapt role examples for different reviewer families
  runbooks/
    resumable-git-audit-pipeline.md ← recommended for external reviewer / multi-CLI workflows
  archive/                         ← empty dir for TYPE-C docs (keep it)

templates/
  project-context.template.md      ← blank project adapter to fill in
  session_state.template.md        ← blank session state to fill in
  roadmap.template.md              ← blank ROADMAP to fill in
  git_audit_task_packet.template.md ← task packet template
  git_audit_receipt.template.md    ← audit receipt template
  git_audit_handoff_packet.template.md ← handoff packet template
  reviewer_role_profile.template.md ← role profile template for external or internal reviewers

scripts/
  git_audit_pipeline.py            ← generator for packet / receipt / handoff assets
```

---

## Step 2 — Fill In the Project Adapter

Open `.github/project-context.instructions.md` and replace every `[placeholder]`:

| Placeholder | Replace with |
|---|---|
| `[Project Name]` | Your project name |
| Project Map rows | Your actual directory structure |
| Canonical Docs rows | Your actual key docs |
| Critical Topic Triggers | Keywords that matter in your domain |
| Build and Test Commands | Your actual build/test/lint commands |
| Protected Paths | Paths that require explicit confirmation before destructive ops |
| Runtime Config Locations | Where your config files live |

Use `templates/project-context.template.md` as a blank starting point if preferred.

If your project will use external Codex, multiple CLI sessions, or explicit reviewer handoff, also keep the `audit|handoff|receipt|packet` trigger mapped to `docs/runbooks/resumable-git-audit-pipeline.md`.

If your project will define multiple reviewer or agent roles with different judgment responsibilities, keep `docs/STRATEGY_MECHANISM_LAYERING.md` and use `templates/reviewer_role_profile.template.md` to formalize them.

When doing so, define the role by judgment boundary first, not by tool name. For example, prefer `runtime correctness reviewer` over `Codex reviewer`, and `maintainability reviewer` over `Claude reviewer`. A CLI, subagent, or custom agent can then be listed as one possible executor of that role.

If you want concrete starting points instead of a blank role profile, keep `docs/ROLE_STRATEGY_EXAMPLES.md` and adapt the examples that fit your repository.

---

## Step 3 — Initialize session_state.md

Copy `templates/session_state.template.md` to the project root as `session_state.md`.

Fill in:
- **Current Goal**: one sentence describing what you are working on right now
- **Working Hypothesis**: state the current working assumption (e.g., "The fix requires X" or "The root cause is Y") — even for well-understood tasks, a brief hypothesis anchors the cognitive loop
- **Confidence**: High / Medium / Low
- **Acceptance Criteria**: the observable conditions that mark your first phase complete

Leave everything else blank or with placeholder text until the first subtask is confirmed done.

---

## Step 4 — Create docs/INDEX.md

Your `docs/INDEX.md` starts with the core docs that exist. For a new project, that might be just:

```markdown
| Document | Description |
|---|---|
| `README.md` | Project entry point |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Agent framework layer design |
| `docs/ADOPTION_GUIDE.md` | How to adopt this framework |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to split role strategy from reusable workflow mechanism |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples to adapt |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable Git audit |
```

Update this index every time you add or remove a TYPE-A document.

---

## Step 5 — Verify docs/archive/ Exists

The `docs/archive/` directory ships with the template (it contains a `.gitkeep`). Confirm it is present after copying:

```bash
ls docs/archive/
```

If it is missing (e.g., some copy tools skip empty-ish directories), recreate it:

```bash
mkdir -p docs/archive
touch docs/archive/.gitkeep
```

All TYPE-C documents (phase reports, one-time analyses, summaries) go here.

---

## Step 6 — Initialize ROADMAP.md

Copy `templates/roadmap.template.md` to the project root as `ROADMAP.md`.

Fill in:
- **Phase 1 name and goal**: one sentence describing what the first phase achieves
- **Initial subtasks**: the work items you know about right now
- **Acceptance criteria**: observable conditions that mark Phase 1 complete

Rules 9 and 10 both write to `ROADMAP.md` (updating rows to `✅ YYYY-MM-DD`), so this file must exist before the agent starts work.

---

## Step 7 — Customize Rule 8 Footer Language (Optional)

The default footer in `copilot-instructions.md` uses English. If your team works in another language, update the footer examples in Rule 8 accordingly.

---

## Step 8 — Remove What You Don't Need

The following files are optional and can be removed for simpler projects:

| File | Remove if... |
|---|---|
| `.github/agents/architect.agent.md` | You don't use separate analysis agents |
| `.github/agents/implementer.agent.md` | Same as above |
| `.github/instructions/backend.instructions.md` | Not a backend project |
| `.github/instructions/docs.instructions.md` | Documentation is minimal |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Team is familiar with the framework |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | You do not need formal reviewer or agent role splits |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | You do not need example reviewer families because you already have your own role model |
| `docs/runbooks/resumable-git-audit-pipeline.md` | No external reviewer, multi-CLI, or resumable handoff workflow is needed |
| `templates/git_audit_*.template.md` + `scripts/git_audit_pipeline.py` | Same as above |
| `templates/reviewer_role_profile.template.md` | Same as above |
| `templates/` | All templates have been applied |

---

## Minimal Viable Setup

If you want the smallest possible setup:

```
.github/
  copilot-instructions.md          ← keep (core rules)
  project-context.instructions.md  ← keep (fill in)

docs/
  INDEX.md                         ← keep (update as docs grow)
  archive/                         ← keep (ships empty)

session_state.md                   ← create from templates/session_state.template.md
ROADMAP.md                         ← create from templates/roadmap.template.md
```

Everything else is additive.

After setup, run `bash scripts/validate-template.sh` from the repo root to confirm no required files are missing.

If you keep the resumable audit workflow, do a smoke run once:

```bash
python scripts/git_audit_pipeline.py init-task \
  --task-id "template-smoke" \
  --goal "Verify packet generation" \
  --truth-sources "- docs/runbooks/resumable-git-audit-pipeline.md" \
  --allowed-files "- docs/**" \
  --do-not-touch "- .env" \
  --validation "- bash scripts/validate-template.sh" \
  --acceptance-boundary "- task packet exists"
```

---

## Ongoing Maintenance

| Trigger | Action |
|---|---|
| New TYPE-A doc added | Update `docs/INDEX.md` |
| Phase complete | Archive to `docs/archive/`, rotate `session_state.md`, mark ROADMAP |
| Protected path changes | Update `project-context.instructions.md` |
| New topic trigger needed | Add row to Critical Topic Triggers in adapter |
| `session_state.md` exceeds ~100 lines | Archive old phase content; keep current phase + insights |

---

## Troubleshooting

**Agent ignores the rules**: confirm `.github/copilot-instructions.md` is being loaded by your AI assistant. Some tools require explicit activation.

**Agent doesn't load the right doc**: check the Critical Topic Triggers in your project adapter — ensure the keyword matches what appears in typical user messages.

**session_state.md is out of sync**: treat the actual code as truth; update session_state.md to match, not the other way around.

**validate-template.sh fails with missing checks**: re-run after copying the latest `copilot-instructions.md` and `scripts/` from this template repository.

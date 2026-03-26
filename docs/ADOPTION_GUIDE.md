# Adoption Guide

Step-by-step guide for adopting this agent framework in a new project.

---

## Prerequisites

- GitHub repository (new or existing)
- A coding assistant that reads `.github/copilot-instructions.md` (GitHub Copilot, Cursor, Augment, etc.)
- A `ROADMAP.md` or equivalent planning document (can be minimal)

---

## Step 1 — Copy the Core Files

Copy these files into your new repository, preserving their paths:

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–10)
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

templates/
  project-context.template.md      ← blank project adapter to fill in
  session_state.template.md        ← blank session state to fill in
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

---

## Step 3 — Initialize session_state.md

Copy `templates/session_state.template.md` to the project root as `session_state.md`.

Fill in:
- **Current Goal**: one sentence describing what you are working on right now
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
```

Update this index every time you add or remove a TYPE-A document.

---

## Step 5 — Create docs/archive/

Create an empty `docs/archive/` directory (add a `.gitkeep` if needed).

This is where all TYPE-C documents (phase reports, one-time analyses, summaries) will live.

```bash
mkdir -p docs/archive
touch docs/archive/.gitkeep
```

---

## Step 6 — Customize Rule 8 Footer Language (Optional)

The default footer in `copilot-instructions.md` uses English. If your team works in another language, update the footer examples in Rule 8 accordingly.

---

## Step 7 — Remove What You Don't Need

The following files are optional and can be removed for simpler projects:

| File | Remove if... |
|---|---|
| `.github/agents/architect.agent.md` | You don't use separate analysis agents |
| `.github/agents/implementer.agent.md` | Same as above |
| `.github/instructions/backend.instructions.md` | Not a backend project |
| `.github/instructions/docs.instructions.md` | Documentation is minimal |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Team is familiar with the framework |
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
  archive/                         ← keep (empty)

session_state.md                   ← create from template
ROADMAP.md                         ← create (can be minimal)
```

Everything else is additive.

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

# Agent Framework Template

A minimal, reusable GitHub Copilot agent framework. Drop it into any project to give your AI coding assistant structured decision rules, state management, and a clean operating protocol.

---

## What's Included

```
.github/
  copilot-instructions.md          ← operating rules (10 rules, always loaded)
  project-context.instructions.md  ← project adapter (fill in for your project)
  agents/
    architect.agent.md             ← analysis / planning / critique agent
    implementer.agent.md           ← execution / validation / change agent
  instructions/
    backend.instructions.md        ← protocol for backend code changes
    docs.instructions.md           ← protocol for documentation changes

docs/
  INDEX.md                         ← navigation index for all TYPE-A docs
  FRAMEWORK_ARCHITECTURE.md        ← how the layer system works
  ADOPTION_GUIDE.md                ← step-by-step setup for a new project

templates/
  project-context.template.md      ← blank project adapter
  session_state.template.md        ← blank cross-session state file
```

---

## Quick Start

### Minimal setup (3 files)

```bash
# 1. Copy the core rules
cp .github/copilot-instructions.md          your-repo/.github/
cp .github/project-context.instructions.md  your-repo/.github/

# 2. Initialize session state
cp templates/session_state.template.md      your-repo/session_state.md

# 3. Fill in the project adapter
#    Edit your-repo/.github/project-context.instructions.md
#    Replace all [placeholders] with real values
```

### Full setup

See [`docs/ADOPTION_GUIDE.md`](docs/ADOPTION_GUIDE.md) for a complete walkthrough.

---

## Core Concepts

**Layered instruction loading** — rules are loaded on-demand, not all at once:

| Layer | File | Loaded when |
|---|---|---|
| 1 — Operating rules | `copilot-instructions.md` | Always |
| 2 — Project adapter | `project-context.instructions.md` | Multi-step task starts / keyword match |
| 3 — Canonical docs | `docs/*.md` | Topic confirmed relevant |
| 4 — Code files | actual source files | Immediately before edit |

**State tracking** — `session_state.md` at repo root tracks:
- Current goal
- Active work and what's completed this phase
- Acceptance criteria
- Technical decisions and durable insights

**Completion checkpoints** — when a subtask is confirmed done, the agent updates ROADMAP, session state, acceptance criteria, and the reply footer before moving on.

---

## Compatibility

Works with any AI coding assistant that loads `.github/copilot-instructions.md`:

- GitHub Copilot (Workspace / Chat)
- Cursor
- Augment Code
- Windsurf
- Any tool that respects `.github/copilot-instructions.md` or a configurable system prompt

---

## Customization Points

| What to customize | Where |
|---|---|
| Project directory map | `project-context.instructions.md` → Project Map |
| Topic → doc routing | `project-context.instructions.md` → Critical Topic Triggers |
| Build/test commands | `project-context.instructions.md` → Build and Test Commands |
| Protected paths | `project-context.instructions.md` → Protected Paths |
| Footer language | `copilot-instructions.md` → Rule 8 |
| Agent roles/format | `.github/agents/*.agent.md` |

---

## License

[Add your license here]

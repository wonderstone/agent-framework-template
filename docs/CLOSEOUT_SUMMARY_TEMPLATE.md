# Closeout Summary Template

This document defines a stable closeout-summary shape for hosts where task completion is driven by a terminal action such as `task_complete`.

For VS Code Copilot-style hosts, this template is meant to be used inside `task_complete.summary` by default.

## Recommended Template

```md
- Result: [one-sentence summary of what was completed]
- Validation: [key command / check / observable evidence]
- Global State: ROADMAP=[current phase status] | session_state=[current overall state]
- Next: [none / next phase / blocked by X]

---
📍 当前聚焦: [final focus] | 已完成: [delivered outcome] | 下一步: [none / next / blocker]
```

## Why This Shape

The closeout body carries the human-readable substance.

The final `---` plus `📍` footer creates a stable visual boundary that is easy to distinguish from mid-task progress updates.

## Global State Field

Recommended shape:

```text
ROADMAP=[Phase N: ✅ done / 【active】 / ○ pending] | session_state=[current goal / current mode / blocked]
```

## Default Recommendation

For adopters of this template, the preferred default is:

```md
- Result: [one-sentence completion summary]
- Validation: [highest-signal evidence]
- Global State: ROADMAP=[phase snapshot] | session_state=[overall state snapshot]
- Next: [none / next phase / explicit blocker]

---
📍 当前聚焦: [final focus] | 已完成: [one-sentence completion summary] | 下一步: [none / next / blocker]
```

## Rules For Good Use

Do:

- keep the body compact and high-signal
- keep exactly one final `📍` footer and place `---` immediately before it

Do not:

- turn the closeout into a second changelog
- use the final `📍` footer more than once in the same task

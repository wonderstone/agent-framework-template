# Root Cause Note

> Use this at closeout when a failure packet exists, the issue was user-visible, the surface was sensitive, or the cause remains only suspected.

---

## Cause Status

- Cause status: [suspected / established]
- Related failure packet: [path]
- Impacted surface: [user-visible surface]

## Cause Statement

- Cause statement: [what the repository believes caused the issue]
- Supporting evidence:
  - [log / command / repro result / diff / inspection finding]

## Fix Statement

- Fix statement: [what changed]
- Why this fix addresses cause rather than symptom alone: [brief reasoning]

## Residual Risk

- What could still go wrong: [remaining risk]
- What would likely be observed first if it does: [earliest signal]

## Validation Summary

- Positive-path validation:
  - [what passed]
- Negative-path or misuse-path validation:
  - [what was checked, or `not required for this issue`]

## Closeout Truthfulness

- Safe to say `closed`: [yes / no]
- If `no`, preferred wording: [mitigated / cause-suspected / awaiting confirmation / custom]

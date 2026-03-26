# Documentation Change Instructions

> Applied whenever a task involves creating, updating, or reorganizing documentation.

## Document Type Classification

Before creating or editing a doc, identify its type:

| Type | Definition | Location |
|---|---|---|
| **TYPE-A** | Long-lived: architecture, runbooks, API specs, adoption guides | `docs/` or module root |
| **TYPE-B** | Module-local, evolves alongside code | module directory |
| **TYPE-C** | Phase reports, one-time analyses, summaries | `docs/archive/` |

**Decision rule**:

```
Will others reference this repeatedly over multiple months?
  YES → TYPE-A (docs/ or module root)
  NO  → TYPE-C (docs/archive/)
```

## Creation Checklist

- [ ] Type classified (A / B / C)
- [ ] Placed in the correct location (see table above)
- [ ] If TYPE-A: `docs/INDEX.md` updated with one-line entry
- [ ] If TYPE-C: creation date noted at top of file
- [ ] Existing docs that this supersedes: marked as superseded or archived

## `docs/INDEX.md` Update Protocol

Every time a TYPE-A doc is **added** or **removed**:

1. Open `docs/INDEX.md`
2. Add or remove the corresponding line: `[filename] — one-sentence description`
3. Keep the index sorted alphabetically within each section

Do not add TYPE-B or TYPE-C entries to `docs/INDEX.md`.

## Editing Existing Docs

- Edit in place — do not create a parallel "v2" file
- If the edit changes an architectural decision, add a dated note at the bottom: `> Updated YYYY-MM-DD: [what changed and why]`
- If the content is fully superseded, archive the old file to `docs/archive/` and add a one-line redirect note at the top of the old path

## Sync Requirements

| Code change | Doc that must stay in sync |
|---|---|
| New module or service | `ARCHITECTURE.md` + `docs/INDEX.md` |
| API change | OpenAPI spec / `docs/API.md` |
| Phase completion | Archive phase report → `docs/archive/Phase_N_*.md` |
| New adoption step | `docs/ADOPTION_GUIDE.md` |

## Post-Change Checklist

- [ ] Doc placed in correct location
- [ ] `docs/INDEX.md` updated (if TYPE-A)
- [ ] No orphaned references to the old doc location
- [ ] Commit message: `docs: [description]`

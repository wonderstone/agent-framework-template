# Backend Change Instructions

> Applied whenever a task involves changes to backend service code, APIs, data models,
> or infrastructure configuration.

## Before You Start

1. Read `.github/project-context.instructions.md` — confirm build/test commands
2. Identify whether the change touches a **public contract** (API, data model, config schema)
3. If yes → cross-module validation required (not just file-level)

## Change Sequence

```
Read target file
  ↓
Make minimal change
  ↓
Run targeted validation (see matrix below)
  ↓
If public contract changed → update docs (openapi, schema docs, etc.)
  ↓
Run cross-module validation
  ↓
Report result + commit-ready summary
```

## Validation Matrix

| Change type | Minimum command |
|---|---|
| Internal implementation detail | `pyright <file>` + `pytest tests/<module>/` |
| Service boundary / API contract | `pyright .` + full test suite + update API docs |
| Config schema or default value | Check all consumers of that config key; smoke test |
| Database migration | Verify migration is reversible; test up + down |

## Doc Sync Requirements

| What changed | What doc to update |
|---|---|
| API endpoint added/removed/modified | OpenAPI spec / `docs/API.md` |
| Data model field added/removed | Schema docs + migration notes |
| New service or module | `ARCHITECTURE.md` + `docs/INDEX.md` |
| Config key added/changed | `docs/CONFIGURATION.md` (or equivalent) |

## Protected Patterns

- Do not change default values in code without also checking runtime override locations
- Do not delete a config key without searching all consumers first
- Do not modify a public interface without updating the corresponding doc

## Post-Change Checklist

- [ ] Validation passed (command + result recorded)
- [ ] Public contract docs updated (if applicable)
- [ ] No unrelated files touched
- [ ] Commit message follows project convention

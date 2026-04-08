# Developer Toolchain Probe Receipt

- Receipt ID: [receipt-id]
- Generated at: [generated-at]
- Repository root: [repository-root]
- Project context: [.github/instructions/project-context.instructions.md]
- Probe mode: [single-surface | all-surfaces]
- Selected surfaces: [selected-surfaces]

## Probe Results

| Surface | Scope | Declared status | Probe outcome | Exit code | Command or source | Fallback or stop | Evidence summary |
|---|---|---|---|---|---|---|---|
| [surface] | [scope] | [declared status] | [success | failure | skipped-known-broken | skipped-explicit-none | not-applicable] | [exit code or `n/a`] | [command] | [fallback or stop] | [short summary] |

## Notes

- Probe receipts are runtime evidence, not automatic canonical status edits.
- A failed probe does not mean the script failed; it means the declared toolchain surface produced evidence that must be handled honestly.
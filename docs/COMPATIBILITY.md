# Compatibility

This document explains what has been verified in this repository and where adopters should still do project-specific validation.

---

## Verified In This Repository

The following are exercised directly in this template repository:

| Surface | Verification |
|---|---|
| Bootstrap CLI | Unit tests plus `--dry-run` smoke commands in CI |
| Template validator | Unit tests plus CI execution |
| Git audit generator | Unit tests |
| Core docs and file references | Structured validator |

The CI workflow currently validates on Python 3.11 and 3.12.

---

## Integration Notes

| Tool or environment | Current status |
|---|---|
| GitHub Copilot-style `.github/copilot-instructions.md` loading | Primary target |
| Cursor / Windsurf / Augment | Intended when they respect the same instruction surface |
| Codex CLI or external CLI reviewer workflows | Supported conceptually by the packet / receipt / handoff mechanism; verify local prompting behavior in your environment |
| Browser, backend, CLI, or library projects | Supported through bootstrap presets, but still require project-specific command customization |

Adopters should treat the bootstrap output as a starting point, not finished project configuration.

---

## Known Limits

- The framework cannot force every AI tool to honor every instruction consistently; tool behavior still varies.
- Bootstrap presets provide sensible defaults, not environment discovery deep enough for every repository.
- The validator checks structure and contract consistency; it does not prove semantic quality of every doc or role profile.
- Example reviewer roles are meant to be adapted, not copied blindly into production governance.

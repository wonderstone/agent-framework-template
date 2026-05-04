# Claude Profile Helpers Skill

## Purpose

Use the existing zsh helper functions to switch Claude Code provider profiles quickly in an interactive shell without typing the lower-level script commands each time.

## When to use

Use this skill when the user wants to:

- switch the current zsh session between Claude-compatible provider profiles
- check which Claude Code profile variables are active
- run a single command under a specific profile without changing the parent shell permanently
- use short helper commands instead of calling `scripts/provider-switch.sh` directly

## Files

- Shell helpers: `shell/provider-switch.zsh`
- Script backend: `scripts/provider-switch.sh`
- README: `README.md`

## Available helpers

- `ccuse <profile>`: apply a profile to the current shell
- `ccrun <profile> <command> [args...]`: run one command with a profile in a subprocess
- `ccstatus`: print current Claude-related environment values
- `ccprofiles`: list supported profiles

Supported profiles:

- `anth`
- `ds-pro`
- `ds-flash`
- `reset`

## How to use

### 1. Load the helper file into zsh

```bash
source shell/provider-switch.zsh
```

### 2. Switch the current shell profile

```bash
ccuse ds-pro
ccuse anth
```

Use `ccuse` when the current terminal session should keep the selected profile for subsequent Claude Code runs.

### 3. Run a single command with a profile

```bash
ccrun ds-flash claude
ccrun ds-pro claude --help
```

Use `ccrun` when the parent shell should stay unchanged.

### 4. Inspect status and available profiles

```bash
ccstatus
ccprofiles
```

## Expected environment

For `ds-pro` and `ds-flash`, make sure `DEEPSEEK_API_KEY` is set in `.env` at the framework root or already exported in the shell.

## Notes

- This skill is for interactive zsh sessions.
- For framework-agnostic or non-interactive usage, prefer the provider-switch skill.
- The zsh helpers delegate to the same backend script, so profile behavior stays consistent across both skills.

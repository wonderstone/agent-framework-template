# Provider Switch Skill

## Purpose

Switch Claude Code between direct Anthropic access and DeepSeek V4 profiles from a shared script so other agent frameworks can reuse the same mechanism.

## When to use

Use this skill when the user wants to:

- switch Claude Code between model providers
- try DeepSeek V4 in Claude Code
- standardize provider selection across multiple agent frameworks
- launch a command with a specific Claude-compatible provider profile

## Files

- Script: `scripts/provider-switch.sh`
- Shell helpers: `shell/provider-switch.zsh`
- README: `README.md`

## Profiles

- `anth`: reset to direct Anthropic-style defaults
- `ds-pro`: DeepSeek V4 Pro through DeepSeek's Anthropic-compatible endpoint
- `ds-flash`: DeepSeek V4 Flash through DeepSeek's Anthropic-compatible endpoint
- `reset`: alias of `anth`

## How to use

### 1. Change the current shell environment

If the framework can source shell scripts:

```bash
source scripts/provider-switch.sh apply ds-pro
```

If the framework cannot source but can evaluate command output:

```bash
eval "$(bash scripts/provider-switch.sh env ds-pro)"
```

### 2. Run one command with a profile

Use this when the framework should not mutate the parent shell:

```bash
bash scripts/provider-switch.sh exec ds-flash claude
```

Examples:

```bash
bash scripts/provider-switch.sh exec ds-pro claude
bash scripts/provider-switch.sh exec anth claude
```

### 3. Inspect the current state

```bash
bash scripts/provider-switch.sh status
```

## Expected environment

For `ds-pro` and `ds-flash`, set:

```bash
DEEPSEEK_API_KEY="your-key-here"
```

Preferred location: `.env` at the framework root.

The script maps Claude Code variables such as:

- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`
- `ANTHROPIC_MODEL`
- `ANTHROPIC_DEFAULT_OPUS_MODEL`
- `ANTHROPIC_DEFAULT_SONNET_MODEL`
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`
- `CLAUDE_CODE_SUBAGENT_MODEL`
- `CLAUDE_CODE_EFFORT_LEVEL`
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- `API_TIMEOUT_MS`

## Notes for other agent frameworks

- Prefer `exec <profile> <command>` if your framework launches subprocesses.
- Prefer `env <profile>` if your framework can capture stdout and export variables itself.
- Use `apply` only in shells that support `source`.
- The script is intentionally provider-agnostic at the call surface so more profiles can be added later.

## Extension pattern

To add a new provider profile later:

1. Edit `scripts/provider-switch.sh`
2. Add the profile name in `profile_exists`
3. Add its environment mapping in `print_exports`
4. Update this `SKILL.md`
5. Update `README.md`

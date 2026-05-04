# Windows SSH Automation

- ID: windows-ssh-automation
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Drive a Windows host from macOS over SSH without losing control to quoting failures, false SCM assumptions, or misleading copied-binary errors.

## Triggers

### Positive Triggers

- Use when a task needs remote Windows inspection, repo sync, service discovery, or runtime evaluation from macOS.
- Use when the agent must decide whether the Windows host is SCM-backed or non-SCM.
- Use when a copied `.exe` behaves differently from a Windows-local build and the execution surface needs to be separated from repository truth.
- Use when a truthful `observe` lane is needed because the backend is already started outside SCM.

### Negative Triggers

- Do not use for local-only Windows work performed directly on the host without SSH.
- Do not use when the task is purely application-level debugging with no remote-host control-plane question.

## Entry Instructions

1. Prefer `powershell -NoProfile -NonInteractive -EncodedCommand <base64-utf16le>` for non-trivial remote commands.
2. Set `COPYFILE_DISABLE=1` before tar-based copies from macOS to Windows.
3. Keep syncs focused; if a large tar stream behaves ambiguously, switch to smaller targeted copies and verify the destination explicitly.
4. Discover the control plane before editing profiles: prefer `Get-CimInstance Win32_Service` filtered by `PathName`, then check scheduled tasks, watchdog scripts, batch launchers, and live process command lines.
5. If the host is not really SCM-backed, keep the lifecycle mode honest and use `observe` rather than inventing `windows_service_name` values.
6. Before blaming the CLI, try a Windows-local build with cache and temp directories pinned to a stable `C:` path. Treat copied-binary crashes and Windows-local build results as different evidence streams.

## Expected Effect

- Remote Windows commands stay reproducible.
- SCM and non-SCM hosts are distinguished truthfully.
- Copied-binary failures do not get misdiagnosed as contract failures if a Windows-local build path still works.
- The evaluation lane produces receipt-bearing evidence instead of hand-wavy host conclusions.

## Working Recipe

### Remote command pattern

```bash
script='Get-CimInstance Win32_Service | Select-Object Name,PathName'
encoded=$(printf "%s" "$script" | iconv -f utf-8 -t utf-16le | base64 | tr -d '\n')
ssh <win-alias> "powershell -NoProfile -NonInteractive -EncodedCommand $encoded"
```

### Focused copy pattern

```bash
COPYFILE_DISABLE=1 tar -cf - -C <local-root> <relative-path> | ssh <win-alias> "tar -xf - -C <windows-root>"
```

### Windows-local Go build pattern

```powershell
$env:GOCACHE = "C:\host-cache\go-build-cache"
$env:GOTMPDIR = "C:\host-cache\go-temp"
$env:TEMP = "C:\host-cache\go-temp"
$env:TMP = "C:\host-cache\go-temp"
go build -o C:\host-cache\remote-win-runtime-local.exe ./cmd/remote-win-runtime
```

If that succeeds while a copied `.exe` still fails, prefer the Windows-local binary for evaluation and treat the copied path as a separate deployment issue.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| skill template | templates/skill.template.md | no | canonical framework skill shape |
| project context adapter | .github/instructions/project-context.instructions.md | yes | project-specific host, repo, and verification facts |

## Governance

### Allowed Evidence

- Receipt-bearing Windows evaluation runs.
- Human-reviewed root-cause notes tied to SSH quoting, service discovery, or copied-binary failures.
- Stable host-operation findings that change future execution order or stop rules.

### Reviewer Gate

- Changes to purpose, triggers, or entry instructions require maintainer review.

### Forbidden Direct Update Inputs

- Raw chat transcripts promoted directly into the skill.
- One-off host quirks with no repeatable execution impact.
- Vendor-specific shell behavior treated as canonical without a degradation note.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `single-reviewer`; no auto-proposed rewrite | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `single-reviewer`; must preserve negative triggers | `delegated-reviewed` |
| `entry_instructions` | `1-3` | `single-reviewer` | `single-reviewer`; must preserve truthful degradation | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; cannot weaken stop rules silently | `delegated-reviewed` |

## Degradation

- If `iconv` or `base64` are unavailable, fall back to the simplest possible one-layer PowerShell command and avoid nested `cmd /c` plus inline script blocks.
- If the host cannot execute copied binaries, do not block the whole task immediately; first test a Windows-local build path.
- If the host is genuinely non-SCM, land truthful `observe` receipts and document the missing lifecycle driver rather than faking a full lifecycle pass.

## Validator Notes

- Keep positive triggers focused on macOS-to-Windows remote execution rather than generic Windows debugging.
- Do not let copied-binary failures erase the distinction between deployment-surface issues and validated Windows-local builds.
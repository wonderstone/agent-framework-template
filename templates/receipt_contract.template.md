# Receipt Contract Template

> **Template type:** adopt-and-customize
> **Scope:** operator evaluation, integration proof, host evidence capture
> **Adopter action:** copy into `docs/receipt-contract.md`, fill bracketed placeholders,
>   replace example lanes/profiles with your repo's actual evaluation surfaces.

---

## 1. Purpose

This contract defines how operator evaluation receipts are stored, named,
verified, and accepted in `<REPO>`. It is derived from real problems observed
across multi-agent Windows host evaluations and is intended to prevent:

- Filename/content mismatch (wrong lane data under a correct-looking name)
- Hardcoded timestamps that overwrite historical evidence
- CLI path defaults that point at known-broken binaries
- README inventories that disagree with disk files and script output

---

## 2. Receipt Directory Naming

**Hard rule:** Every evaluation run creates a new UTC-timestamped directory.
Never hardcode a fixed timestamp in scripts or documentation.

```
<receipt-root>/<YYYYMMDDTHHmmssZ>/
```

| Field | Rule |
|---|---|
| Format | `yyyyMMddTHHmmssZ` (ISO 8601 compact, UTC, no separators) |
| Generation | Runtime-generated: `(Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")` |
| Immutability | Read-only after evaluation run completes. Correct only via correction protocol (§8). |
| Active pointer | Declared in a single discovered-metadata file (e.g., `operator-evaluation.discovered.json`) |

**Example** (from `remote-win-runtime`):
Directory `20260502T075129Z` was generated at runtime by
`run-readonly-receipts.ps1`. The prior directory `20260502T120000Z`
was deleted after its read-only receipts were found to have
filename/content mismatch.

---

## 3. Step File Naming

**Hard rule:** The filename must make the lane and step inferrable without
reading the README. Do not rely on the README to disambiguate.

### Read-only evaluation files (no lease, no mutation)

Use a 2-digit numeric prefix:

```
01-<command>-<lane-or-profile>.json
02-<command>-<lane-or-profile>.json
...
```

**Example** (from `remote-win-runtime`):
```
01-backend-status-batch-command.json
02-doctor-batch-command.json
03-backend-status-scheduled-task-watchdog.json
04-doctor-scheduled-task-watchdog.json
```

### Lifecycle evaluation files (mutating, lease-gated)

Use `L` + single-digit prefix:

```
L1-<step-name>.json
L2-<step-name>.json
...
```

**Example** (from `remote-win-runtime`):
```
L1-lease-acquire.json
L2-profile-activate.json
L3-health-wait-ready.json
L4-doctor-after-ready.json
L5-state-show.json
L6-backend-stop.json
L7-lease-release.json
```

### Content verification rule

**Hard rule:** After capture, verify that each receipt file's content matches
its filename. Minimum check: compare `data.active_profile` (or equivalent)
against the expected lane/profile for that file.

**Historical lesson (remote-win-runtime 20260502T120000Z):**
`01-backend-status-batch-command.json` contained `active_profile: flux-dev-watchdog`
and `control_plane_mode: scheduled-task-watchdog` — watchdog data under a
batch-command filename. The fix required re-capturing all four read-only receipts
into a new directory and deleting the old one.

---

## 4. Supporting Files (Minimum Set)

**Hard rule:** Every receipt directory must contain at minimum:

| File | Required When | Description |
|---|---|---|
| `README.md` | Always | Inventory table, key findings, operator notes, production blockers |
| `host-state.json` | Always | State file used during evaluation (establishes pre-conditions) |
| `host-state.events.jsonl` | Any mutation step run | Event log captured during lifecycle mutation |
| `host-state.final.json` | Any mutation step run | State file after last mutation step |
| `operator-notes.txt` | Recommended | Free-text operator observations during the run |

---

## 5. README Inventory (Minimum Fields)

**Hard rule:** The README inventory table must agree with both the files on
disk and the script output naming convention. All three sources must match.

### Read-only section columns

| Column | Source field |
|---|---|
| File | filename in directory |
| Profile | `data.active_profile` or `data.checked_profile` from receipt |
| Control Plane | `data.control_plane_mode` from receipt |
| Result | `ok` + key observation |

### Lifecycle section columns

| Column | Source field |
|---|---|
| Step | L1 through LN |
| File | filename in directory |
| Result | `ok` + key evidence (e.g., probe attempts, HTTP status) |

### Additional sections (recommended)

- **Key Findings** — per-lane conclusions (success / prereq gap / failure)
- **Contract Honesty** — verify `driver_capabilities`, `lifecycle_observation`,
  and control-plane mode fields are present and mode-aware in every envelope
- **Production Blockers** — operator-confirmed values still required

**Historical lesson (remote-win-runtime README/L1-L7/05-11 split):**
The README inventory used `05-` through `11-` filenames while the script
produced `L1-` through `L7-` and the disk files were in the old naming.
A reviewer flagged the three-source disagreement. Fix: rename files on
disk, update README, keep script output as the canonical naming.

---

## 6. Historical vs Active Receipts

**Hard rule:** Distinguish contract-only receipts from real-host receipts.

| Type | Description | Evidence value |
|---|---|---|
| Contract-only | Captured on any platform; proves envelope shape stability | Confirms format, not host behavior |
| Real-host | Captured on the target host with live probes and process observation | Confirms host behavior |

The active receipt directory is always the most recent real-host receipt.
It is declared in a single metadata file (e.g., `operator-evaluation.discovered.json`
under an `active_receipt_dir` key).

---

## 7. CLI Path Default

**Hard rule:** The default CLI execution path in all scripts and documentation
must be a path that is verified to work on the target host. Do not default to
a known-broken binary.

- If a pre-built binary is known to crash, document it as "not recommended"
  or "requires rebuild" — never as the default.
- If the reliable path is `go run ./cmd/<binary>`, make that the default.
- If a native rebuild script exists, reference it for distributable builds.

**Historical lesson (remote-win-runtime exe crash):**
`remote-win-runtime.exe` cross-compiled from macOS crashed with 0xc0000005.
Scripts and runbook defaulted to it. After diagnosis, the default was changed
to `go run ./cmd/remote-win-runtime` and a `build-windows-binary.ps1` was
added for native Windows builds.

---

## 8. Correction Protocol

**Hard rule:** When a receipt is found to be untruthful:

1. Do NOT rename the file and claim it's now correct.
2. Do NOT edit the JSON content of an existing receipt.
3. Re-capture on the real host into a new timestamp directory.
4. If only a subset is affected, copy truthful receipts from the old
   directory, then delete the old directory.
5. Update the active receipt directory pointer.
6. Document what was wrong and what was corrected in the new README.

---

## 9. Owner Acceptance Checklist

**Hard rule:** Before accepting a receipt directory, verify:

| Check | How |
|---|---|
| All files listed in README exist on disk | `ls` vs README inventory |
| Every receipt filename matches its JSON content | spot-check `data.active_profile` or equivalent |
| All JSON files parse | `python3 -c "import json; json.load(open(f))"` for each |
| README, script output, and disk files agree on naming | no stale naming in any source |
| No hardcoded timestamps in helper scripts | grep for fixed timestamp strings |
| CLI default path is truthful for the target host | no known-broken binary as default |
| Prerequisite gaps are documented as gaps | "blocked" not "completed" for missing prereqs |
| Active receipt pointer is correct | exact path match |

---

## 10. Adopter Customization

Replace these placeholders when adopting:

| Placeholder | What to fill |
|---|---|
| `<REPO>` | Your repository name |
| `<receipt-root>` | Your receipt storage path |
| `<command>` | Your CLI command names |
| `<lane-or-profile>` | Your evaluation lanes or profile names |
| `<step-name>` | Your lifecycle step names |
| `data.active_profile` | Your state field equivalent |
| `data.control_plane_mode` | Your control-plane mode field equivalent |
| `operator-evaluation.discovered.json` | Your operator metadata file |

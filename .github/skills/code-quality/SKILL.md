---
name: code-quality
description: >-
  Multi-dimensional code review and quality enforcement. Reviews code across
  8 dimensions (correctness, security, readability, performance, test coverage,
  error handling, naming, documentation) with severity ranking (CRITICAL/MAJOR/
  MINOR/SUGGESTION). Enforces verification discipline — evidence before assertion.
  Detects code smells, proposes concrete fixes, and gates on quality standards.
  Use when reviewing PRs, pre-merge checks, quality audits, or setting up
  automated quality gates.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Edit
user-invocable: true
---

# Code Quality — Multi-Dimensional Review & Enforcement

You review code with discipline across 8 dimensions, rank findings by severity, and enforce verification — evidence before assertion, always. You are not a rubber stamp. Every comment must reference a real issue with a file:line and a concrete suggestion.

## When to Activate

- BEFORE merging any change to main
- BEFORE opening a PR for external review
- AFTER completing a non-trivial implementation task
- When the user asks for a code review, quality check, or "look over this code"
- When setting up or auditing quality standards for a project

---

## Step 0 — Gather Evidence

Before reviewing, collect:

1. **Change scope** — all files modified, created, or deleted (use `git diff --name-only` or Glob)
2. **Spec/plan** that motivated the change (if available)
3. **Project conventions** — CLAUDE.md, eslint config, tsconfig, project README
4. **Automated check output:**
   - Type check: `tsc --noEmit` / `mypy` / `go build`
   - Tests: `npm test` / `pytest` / `go test ./...`
   - Lint: `eslint` / `ruff check` / `golangci-lint`
5. **Test coverage** for changed code (if available)

If any automated check fails: report it as a CRITICAL finding immediately. The review does not proceed past failing checks.

---

## 8 Review Dimensions (In Priority Order)

### 1. Correctness — Does it solve the stated problem?

- Does the change actually address the spec/issue?
- Are edge cases handled? (empty input, null/undefined, boundary values, error states)
- Is the logic sound? Can you construct an input that produces the wrong output?
- Are there off-by-one errors, inverted conditions, missing cases in a switch?

### 2. Security — Can an attacker exploit this?

- Any user input used without validation?
- Any user input in SQL queries, shell commands, file paths, HTML output?
- Are auth checks present and correct? (Not just client-side guards)
- Are secrets hardcoded? Are environment variables properly scoped?
- Does the change introduce new attack surface (new endpoints, file uploads, webhooks)?

### 3. Readability — Can a colleague understand this in one reading?

- Is the control flow obvious? Or does it require mental backtracking?
- Deep nesting (>3 levels) → suggest early returns
- Long functions (>50 lines) → suggest extraction
- Complex boolean expressions → suggest named intermediate variables
- Comments that explain WHAT → flag as unnecessary (code should be clear)

### 4. Performance — Is there an algorithmic or I/O problem?

- N+1 queries: does a loop contain a DB/API call? → suggest batching with DataLoader/in-batch
- Unnecessary work: repeated computation, redundant re-renders, unnecessary allocations
- Missing memoization on expensive computations in render paths (verify with profiler first)
- Large synchronous operations blocking the event loop (Node.js) or main thread (browser)
- Missing pagination on unbounded queries (every `SELECT *` without LIMIT on a growing table)
- **Bundle size** — new dependency added? Import cost? Tree-shaking verified? Check with `bundlephobia` or `vite-bundle-visualizer`.
- **Query plan regression** — did you add an index? Does the new query use it? Run `EXPLAIN ANALYZE` on new queries against production-like data.
- **Core Web Vitals** — LCP (Largest Contentful Paint) <2.5s, INP (Interaction to Next Paint) <200ms, CLS (Cumulative Layout Shift) <0.1.
- **Memory** — are large arrays/materialized views held in memory indefinitely? Streaming/pagination for large datasets?
- **Cache strategy** — is the cache invalidation correct? Is there a stampede risk on cold start?

### 5. Test Coverage — Are the changes tested?

- New behavior: is there a test for it?
- Bug fixes: is there a regression test that fails before the fix?
- Edge cases: are they covered?
- Test quality: do tests assert behavior (not implementation details)?

### 6. Error Handling — Do failures surface clearly?

- Are errors caught at boundaries? (API handlers, DB calls, external services)
- Are errors silently swallowed? (`catch {}` with no handling)
- Do error messages leak sensitive information? (stack traces, internal paths)
- Are user-facing errors actionable? Or just "An error occurred"?

### 7. Naming — Do names reveal intent?

- Variables: does the name say what it IS, not what it DOES?
- Functions: verb-noun pattern (`fetchUser`, not `user`)
- Booleans: `is`, `has`, `should` prefix (`isActive`, not `active`)
- Collections: plural (`users`, not `userList`)
- Consistent terminology across the codebase (same concept, same name)

### 8. Documentation — Is the WHY documented?

- Public API: documented? (JSDoc, docstrings for exported functions)
- Non-obvious decisions: explained? (why this approach, not another)
- Does the comment explain WHY, not WHAT? (WHAT should be in the code)

### 9. Accessibility (a11y) — Can everyone use this?

- **Semantic HTML.** `<button>` not `<div onclick>`, `<nav>` not `<div class="nav">`. Screen readers depend on native semantics.
- **Keyboard navigation.** Every interactive element reachable and operable via Tab/Enter/Escape. Focus order matches visual order. No focus traps (except modals — with escape).
- **ARIA when necessary.** Use native HTML first. ARIA is a polyfill for missing semantics. `aria-label` on icon-only buttons. `aria-expanded` on toggles. `aria-live` for dynamic content announcements.
- **Color contrast.** Text ≥4.5:1 ratio against background (WCAG AA). Large text ≥3:1. Check with axe DevTools or Lighthouse.
- **Screen reader text.** Visually hidden but accessible: `.sr-only` class for context that sighted users get from layout.
- **Focus management.** After navigation/route change, move focus to new content heading. After modal opens, trap focus inside. After modal closes, return focus to trigger.
- **Form labels.** Every input must have a visible `<label>` or `aria-label`. Placeholder text is NOT a label.
- **Alt text.** Every `<img>` has meaningful `alt` (or `alt=""` if decorative). Complex images (charts) need longer description nearby.

### 10. Internationalization (i18n) — Is it ready for the world?

- **No hardcoded strings in UI.** All user-visible text externalized to i18n keys (`t('order.confirmed')`, not `'Order Confirmed'`).
- **Date/time/numbers.** Use `Intl.DateTimeFormat` / `Intl.NumberFormat`, not `.toLocaleDateString()` with fixed locale. Server-rendered dates should carry timezone context.
- **RTL (Right-to-Left) readiness.** CSS uses logical properties (`margin-inline-start`, not `margin-left`). Flexbox/grid direction flips automatically. Text alignment uses `start`/`end`, not `left`/`right`.
- **String interpolation.** Use named placeholders (`{name} ordered {count} items`), not positional (`%s ordered %d items`). Different languages reorder sentence parts.
- **Pluralization.** Use ICU MessageFormat or i18n library plurals (`{count, plural, one {# item} other {# items}}`), not inline `count > 1 ? 'items' : 'item'`.
- **Locale-sensitive formatting.** Currency, units, phone numbers — all locale-dependent. Don't assume `$` means USD or dates are MM/DD/YYYY.

---

## Severity Ranking

```
Per finding, what severity?

├─ CRITICAL → blocks merge
│   Correctness bug (wrong output, data corruption)
│   Security hole (injection, auth bypass, data leak)
│   Data loss risk
│   Broken build, failing tests, type errors
│
├─ MAJOR → must fix before merge
│   Missing test for new behavior
│   Performance regression (N+1, memory leak)
│   Error swallowing without logging
│   API contract break (removed field, changed type)
│   Missing auth check on new endpoint
│
├─ MINOR → should fix, but doesn't block
│   Confusing naming
│   Function slightly too long (50-80 lines)
│   Duplicate code (2 occurrences)
│   Missing type annotation
│   Comment that restates the code
│
└─ SUGGESTION → optional improvement
    Alternative approach worth considering
    Style preference (matches convention but could be cleaner)
    Potential future refactoring (not in current scope)
```

**Decision rule:**
- Any CRITICAL → BLOCKED (do not merge)
- Any MAJOR → APPROVED WITH NOTES (fix before merge)
- Only MINOR/SUGGESTION → APPROVED

---

## Review Procedure

1. **Map change scope** — read every changed file, understand the change's purpose
2. **For each file:** review against all 8 dimensions
3. **Run automated checks** — typecheck, tests, lint (if not already run)
4. **Collect findings** — file:line + severity + description + suggested fix
5. **Rank by severity**
6. **Structural-change check** — if the diff renames, moves, extracts, or deletes a public symbol:
   - Identify changed symbols
   - Grep for all callers
   - Verify all callers are updated in the same diff, OR documented as breaking change
   - If breaking change without migration note → CRITICAL
7. **Output report**

---

## Output Contract

```markdown
## Code Review — <branch/PR/target>

### Summary
- Files changed: N
- CRITICAL: N | MAJOR: N | MINOR: N | SUGGESTION: N

---

### CRITICAL (N findings)

#### <file>:<line> — <one-line summary>
**Dimension:** Correctness | Security | Performance | ...
**Issue:** <what's wrong, specifically>
**Fix:** <concrete suggestion>

---

### MAJOR (N findings)
...

### MINOR (N findings)
...

### SUGGESTION (N findings)
...

---

### Automated Checks
- Type check: PASS | FAIL
- Tests: N passing, 0 failing
- Lint: N warnings, 0 errors

### Verdict: APPROVED | APPROVED WITH NOTES | BLOCKED

### Evidence
<typecheck/test/lint command output, verbatim>
```

---

## Verification Discipline (from supervibe)

**Evidence before assertion, always.** Before claiming anything "works", "passes", or "is fixed", you MUST:

1. Run the relevant command via Bash
2. Show the full output (stdout + stderr, exit code)
3. Match the claim to the evidence

```
Claim: "Tests pass"
Command: npx vitest run
Exit code: 0
Output (verbatim):
  ✓ src/order.test.ts (12 tests) 45ms
Verdict: PASS
```

**Never:**
- Claim tests pass without running them
- Paraphrase command output (paste verbatim)
- Say "it should work" — show it works
- Skip verification because "this is obviously fine"

---

## Code Smell Detection (Write-Time Quality)

In addition to review, proactively flag code smells during editing. When you write or edit a file, self-check:

### Smells to catch and fix immediately:

| Smell | Fix |
|-------|-----|
| `any` type (TypeScript) | Replace with `unknown` or proper type |
| `var` declaration | Replace with `const` or `let` |
| String concatenation in SQL | Replace with parameterized query |
| `console.log` left in production code | Replace with proper logger or remove |
| Commented-out code | Delete |
| Unused import | Remove |
| Direct mutation of props/state | Replace with immutable update |
| `==` instead of `===` (JS) | Fix to `===` |
| Empty catch block | At minimum, log the error |
| `as` cast without validation (TS) | Add runtime validation or use type guard |
| `eval()` or `new Function()` | Find a safer alternative |
| Hardcoded credentials/secrets | Move to environment variable |

### Quality gates during edits:

- After editing a file, run the project's formatter if available
- After changing function signatures, grep for all callers and update them
- After adding a new exported symbol, verify it follows naming conventions
- If a file exceeds 300 lines, flag it as a candidate for splitting

---

## Automated Quality Enforcement

For projects wanting write-time quality enforcement, integrate these hooks pattern (from Plankton methodology):

### PostToolUse Hook — Multi-Phase Quality

```
Phase 1: Auto-Format (silent)
  → Run formatter (prettier, biome, ruff format, gofmt)
  → Fix 40-50% of issues silently

Phase 2: Collect Violations (JSON)
  → Run linters, collect unfixable violations
  → Structured output: {line, column, code, message, linter}

Phase 3: Delegate + Verify
  → Spawn subprocess to fix violations
  → Re-run Phase 1+2 to verify
  → Exit 0 if clean
```

Only violations the subprocess can't fix are reported to the main agent.

### Config Protection

Linter config files (`.eslintrc`, `.ruff.toml`, `biome.json`, `tsconfig.json`, `pyproject.toml`) should never be modified to suppress violations instead of fixing code. If a config change is proposed, flag it explicitly.

---

## Incremental Quality Strategy (Legacy Code)

Not every codebase starts clean. When reviewing a legacy project with thousands of existing issues:

### The Campground Rule

**Always leave the codebase cleaner than you found it.** Every PR should nudge quality forward, not just avoid regressions. But don't block a 5-line bug fix on "also refactor the 2000-line file."

### Technical Debt Prioritization

```
Rate every issue on two axes (1-10):

Impact: How much does this cost us?
  - 10: Causes production incidents monthly
  - 5: Slows down development noticeably
  - 1: Minor annoyance

Fix Cost: How hard is this to fix?
  - 10: Requires multi-team coordination, months of work
  - 5: A sprint of focused work
  - 1: Single developer, single afternoon

Priority = Impact / Cost
  → High-impact, low-cost fixes FIRST (the "quick wins")
  → High-impact, high-cost fixes get planned into roadmap
  → Low-impact, low-cost fixes get done "when passing through"
  → Low-impact, high-cost fixes get documented as "accepted risk"
```

### Incremental Migration

1. **Set a quality baseline for new/changed code.** Old code can stay as-is until touched. But any file you modify must pass the quality gate for the lines you changed.
2. **Use `eslint --fix` / `ruff --fix` on changed files only.** Don't auto-format the whole project (creates giant, unreviewable diffs).
3. **Add a test before refactoring.** If the legacy code has no tests, write characterization tests that capture current behavior. Then refactor.
4. **Track the trend.** Total lint violations should go DOWN over time. If it's going up, quality is being sacrificed for speed.

### When to Do a Big Cleanup

| Signal | Action |
|---|---|
| Same file modified >10 times/month | Worth a full refactor |
| Onboarding takes >2 weeks because of code quality | Worth stopping feature work to clean |
| Production incidents traced to "confusing code" 3+ times | That module needs priority refactor |
| Lint violations per file >50 | Extract + rewrite the module |

---

## Build Reproducibility

- **Lockfile committed.** `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `Cargo.lock` / `poetry.lock` must be in version control. Without it, CI and production may install different versions than development.
- **Frozen install in CI.** `npm ci` (not `npm install`), `pnpm install --frozen-lockfile`, `yarn install --immutable`. If the lockfile is stale, the build should FAIL, not silently update it.
- **Pinned CI tool versions.** `actions/setup-node@v4` can change behavior between minor versions. Pin by SHA for reproducible builds: `actions/setup-node@11bd719... # v4.2.2`.
- **Container base images pinned by SHA.** `FROM node:22@sha256:abc...` — immutable. `FROM node:22` — floats, can break your build when upstream updates.
- **Deterministic dependency resolution.** `npm` with `--legacy-peer-deps` in one place and not another → different `node_modules`. Standardize install command across local dev, CI, and Docker build.
- **Environment-conditional dependencies.** `if (process.env.NODE_ENV === 'development') require('dev-tool')` — tree-shaking may or may not remove this. Use separate `devDependencies` and `production` install.

---

## Quality Standards — Universal Principles

These apply regardless of language or framework:

### KISS — Keep It Simple, Stupid
- Simplest solution that meets the requirements
- No premature optimization
- Easy to understand > clever code
- If you need to explain it, it's too complex

### DRY — Don't Repeat Yourself
- 3+ occurrences = extract to shared function/module
- 2 occurrences = judge based on likelihood of a third
- But don't DRY things that are coincidentally similar but semantically different

### YAGNI — You Aren't Gonna Need It
- Don't build features before they're needed
- Don't add abstraction layers "for the future"
- Delete unused code; git history preserves it
- "When in doubt, leave it out"

### Immutability by Default (JS/TS)
```typescript
// Good
const updated = { ...obj, field: newValue }
const appended = [...arr, newItem]

// Bad
obj.field = newValue
arr.push(newItem)
```

### Error Handling — Fail Fast, Fail Loud
```typescript
// Good: validate at boundaries
function createUser(input: unknown): User {
  const validated = CreateUserSchema.parse(input) // throws if invalid
  return db.user.create(validated)
}

// Bad: silently return null
function createUser(input: any): User | null {
  try { return db.user.create(input) }
  catch { return null }
}
```

### Testing — AAA Pattern
```typescript
test('returns empty array when no matches', () => {
  // Arrange
  const query = 'nonexistent'

  // Act
  const result = search(query)

  // Assert
  expect(result).toEqual([])
})
```

---

## Guard Rails

- **Don't rubber-stamp.** "LGTM" without specifics is not a review.
- **Don't nitpick without substance.** Every comment must reference a real issue, not a style preference.
- **Don't suggest changes outside the diff scope.** File a separate refactoring task.
- **Don't claim "I tested it" without showing command output.**
- **Always cite file:line for every finding.**
- **Always distinguish blocking (CRITICAL/MAJOR) from advisory (MINOR/SUGGESTION).**
- **Skip structural-change check on rename:** silent breakage waiting to happen. Every rename/move/extract of a public symbol requires caller verification.
- **For pure-additive diffs:** stamp "Structural change: none" explicitly.

## Verification of This Skill

- Every CRITICAL finding has evidence (test failure, reproducer, or clear exploit path)
- Verdict matches finding severity (any CRITICAL → BLOCKED)
- Test/typecheck/lint output included verbatim
- For diffs touching public symbols: caller verification cited

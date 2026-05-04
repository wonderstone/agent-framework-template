---
name: code-refactor
description: >-
  Systematic code refactoring — detect code smells, apply safe transformations,
  and verify behavior preservation. Covers extraction, inlining, renaming,
  deduplication, dead code removal, and structural simplification across
  TypeScript, Python, Go, and Java. Use when the user asks to refactor code,
  improve structure, remove duplication, clean up dead code, simplify logic,
  or apply specific refactoring operations.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Edit
user-invocable: true
---

# Code Refactor — Systematic, Safe Restructuring

You refactor code with discipline: preserve behavior, verify with tests, and leave the codebase cleaner than you found it. You never refactor for the sake of it — every change has a concrete, articulable benefit.

## When to Activate

- User asks to refactor, clean up, simplify, or restructure code
- Code review revealed structural issues (long functions, deep nesting, duplication)
- After a feature is complete and tests pass — improve structure before moving on
- Preparing a module for a new feature that the current structure can't cleanly support
- Dead code or unused dependencies need removal

## Refactoring Philosophy

1. **Behavior preservation is non-negotiable.** The program must do exactly what it did before — unless the user explicitly requests a behavior change.
2. **Tests are your safety net.** If tests exist, run them before and after. If they don't, note that as a risk.
3. **Smallest change that achieves the goal.** One refactoring operation at a time. Don't bundle "while I'm here" changes.
4. **Boy Scout rule.** Leave the code cleaner than you found it — but within scope. Don't refactor adjacent files "while you're passing through."

---

## Phase 0 — Determine Scope

**Actions:**
1. Run `git rev-parse --is-inside-work-tree` to check if in a repo
2. Normalize arguments — trim whitespace, preserve quoted path segments
3. Resolve scope:

```
Arguments provided?
├─ Valid file paths → use as refactoring scope
├─ Valid directory paths → scope to all source files within
├─ Not paths (semantic query) → Grep codebase for matches, then scope to matching files
└─ No arguments → run `git diff --name-only` for recently modified files
```

4. If no files found in any branch: inform user, exit.
5. For project-wide scope, tell the user to use the explicit path or `--all` flag.

## Phase 1 — Analyze (Read & Diagnose)

Read every file in scope. For each file, produce a diagnosis:

### Code Smell Catalog

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| **Long function** (>50 lines) | Count lines between `function`/`def`/`func` declarations | Extract Method — extract logical blocks into named functions |
| **Deep nesting** (≥4 levels) | Count `if`/`for`/`while`/`switch` depth | Early returns, extract condition to variable, invert condition |
| **Duplicate code** (>6 identical lines) | Visual inspection + grep for similar blocks | Extract Method or Extract Module |
| **Large parameter list** (>4 params) | Count function parameters | Introduce Parameter Object |
| **Primitive obsession** | Strings/numbers used where a type is clearer | Replace Primitive with Value Object |
| **Feature envy** | Function calls more methods on another class than its own | Move Method |
| **God class** (>300 lines or >10 public methods) | Count lines and public methods per class | Extract Class — split by responsibility |
| **Data clumps** | Same 3+ fields appearing together in multiple places | Extract Class |
| **Switch/matching on type** | `switch`/`if instanceof` on a type field | Replace Conditional with Polymorphism |
| **Comments explaining WHAT** | Comment restates the code on the next line | Delete comment (code is self-documenting) |
| **Commented-out code** | Block comments containing code | Delete — git history preserves it |
| **Dead code** | Unused exports, functions, variables, types | Delete (after verifying no callers) |
| **Mutable global state** | Module-level `let`, global singletons | Encapsulate, pass as parameter |
| **Inconsistent naming** | Same concept named differently across files | Rename for consistency |
| **Magic numbers** | Unnamed numeric literals in logic | Extract to named constant |

### Diagnosis Output

For each file, produce a brief list:

```
File: src/services/order.ts
  - Long function: processOrder() — 87 lines → Extract Method (validate, persist, notify)
  - Duplicate code: date formatting logic also in src/utils/dates.ts
  - Magic numbers: 100, 0.2, 30 → Extract constants
```

Show this diagnosis to the user. Let them approve or adjust before making changes.

## Phase 2 — Execute (Transform)

Apply refactorings one at a time. After each transformation, verify tests pass (if they exist).

### Refactoring Recipe: Extract Method

```
Before:
function processOrder(order: Order) {
  // 20 lines of validation
  if (!order.items.length) { ... }
  if (order.total < 0) { ... }
  // ...
  // 15 lines of persistence
  // 10 lines of notification
}

After:
function processOrder(order: Order) {
  validateOrder(order)
  const saved = await persistOrder(order)
  await notifyCustomer(saved)
}

function validateOrder(order: Order) { /* validation logic */ }
async function persistOrder(order: Order) { /* persistence logic */ }
async function notifyCustomer(order: Order) { /* notification logic */ }
```

**Rule:** Extracted function name must describe WHAT it does, not HOW. `validateOrder`, not `checkFieldsAndThrow`.

### Refactoring Recipe: Early Return (Flatten Nesting)

```
Before:
if (user) {
  if (user.isActive) {
    if (order) {
      if (order.isPaid) {
        ship(order)
      }
    }
  }
}

After:
if (!user) return
if (!user.isActive) return
if (!order) return
if (!order.isPaid) return
ship(order)
```

### Refactoring Recipe: Replace Primitive with Value Object

```
Before:
function createUser(email: string, name: string, age: number) { ... }

After:
class Email {
  constructor(private readonly value: string) {
    if (!value.includes('@')) throw new Error('Invalid email')
  }
  toString() { return this.value }
}
function createUser(email: Email, name: Name, age: Age) { ... }
```

### Refactoring Recipe: Introduce Parameter Object

```
Before:
function search(query: string, limit: number, offset: number, sortBy: string, order: 'asc' | 'desc')

After:
interface SearchParams {
  query: string
  limit: number
  offset: number
  sortBy: string
  order: 'asc' | 'desc'
}
function search(params: SearchParams)
```

### Refactoring Recipe: Remove Dead Code

**Verification steps before deleting:**
1. Grep for the symbol name across the project
2. Check it's not exported and consumed elsewhere (for internal functions)
3. If exported, search broader (monorepo, published package consumers)

```
Types of dead code and action:
- Unused import → Delete
- Unused variable → Delete
- Unused private function → Delete  
- Unused exported function → Delete export keyword first, then delete if internal only
- Commented-out code block → Delete (git has it)
- `_unusedVar` → Delete, don't rename to suppress warnings
```

### Refactoring Recipe: Remove Duplication

```
Before:
// In file A
const createdAt = new Date(order.createdAt).toLocaleDateString('zh-CN')
// In file B  
const createdAt = new Date(user.createdAt).toLocaleDateString('zh-CN')

After:
// In shared/utils/date.ts
export function formatDate(iso: string, locale = 'zh-CN'): string {
  return new Date(iso).toLocaleDateString(locale)
}

// In file A and B
import { formatDate } from '@/utils/date'
const createdAt = formatDate(order.createdAt)
```

**Rule:** 3+ occurrences = extract. 2 occurrences = judge based on likelihood of a third. 1 occurrence = leave it.

### Language-Specific Refactorings

**TypeScript:**
- Replace `any` with `unknown` + type guards
- Replace function expressions with arrow functions where `this` is not needed
- Replace promise `.then()` chains with `async/await`
- Remove unnecessary `await` (returning a promise directly)
- Replace string concatenation with template literals

**Python:**
- Replace `for i in range(len(x))` with `for item in x` or `enumerate(x)`
- Replace `if x in list` with `if x in set` when repeated lookups
- Replace manual file close with `with` statement
- Replace `%` formatting and `.format()` with f-strings
- Replace list-building loops with list comprehensions

**Go:**
- Replace `if err != nil { return err }` repetition with error propagation helpers where appropriate
- Replace mutex-protected maps with `sync.Map` for high-concurrency read-mostly workloads
- Replace string concatenation in loops with `strings.Builder`

**Java:**
- Replace field injection (`@Autowired private X x`) with constructor injection
- Replace `Optional.get()` without `isPresent()` check with `orElseThrow()`
- Replace raw `String` with `record` or `@Value` for immutable data carriers
- Replace `for`-loop collection building with `Stream.collect()`

**Rust:**
- Replace `match` on `Option`/`Result` with `?` operator for error propagation
- Replace manual `clone()` chains with borrow-based design
- Replace `unwrap()` / `expect()` in library code with `Result` propagation
- Replace `for`-loop with iterator combinators (`map`/`filter`/`fold`)

### Complexity Metrics

Beyond smell counts, use quantitative measures:

| Metric | Threshold | Refactoring |
|--------|-----------|-------------|
| **Cyclomatic Complexity** | >15 per function | Extract branches into separate functions |
| **Cognitive Complexity** | >15 per function | Flatten nesting, extract condition variables |
| **Lines per File** | >300 | Split by responsibility |
| **Lines per Function** | >50 (TS/Python), >80 (Go/Java/Rust) | Extract Method |
| **Parameters per Function** | >4 | Introduce Parameter Object |
| **Public Methods per Class** | >10 | Extract Class — split by responsibility |
| **Afferent Coupling (Ca)** | >20 classes depend on this | Split interface or introduce Facade |
| **Dependency Depth** | >5 layers of imports | Introduce intermediate abstraction |

**Language-specific thresholds:**

Python: 50-line function is already too long (dynamic typing = cognitive load per line is higher). Go: 80-line function may be fine (explicit error handling adds lines without adding complexity). TypeScript: depends on types — well-typed 60-line function better than untyped 30-line function.

### AST Tooling for Safe Refactoring

For large-scale or cross-file refactoring, prefer AST tools over regex:

```bash
# JavaScript/TypeScript — jscodeshift
npx jscodeshift -t transform.ts src/ --parser=tsx

# Multi-language — comby (structural search/replace, not regex)
comby 'oldFunction(:[args])' 'newFunction(:[args])' .ts -i

# Go — gorename (reliable, type-aware)
gorename -from '"pkg".OldName' -to 'NewName'

# Python — rope / libcst
python -m libcst.tool codemod transform.TransformVisitor src/
```

**When to use AST tools:** Renaming symbols across >5 files, changing function signatures that affect >10 call sites, migrating deprecated API usage project-wide.

**When NOT to use AST tools:** Single-file refactoring (manual is faster), logic changes that can't be structurally described, language without mature AST tooling.

### Large-Scale Refactoring (Monorepo / Multi-Package)

1. **Characterize behavior before touching anything.** Write characterization tests (golden master tests) that capture current outputs. These ARE NOT unit tests — they don't validate correctness, they capture CURRENT behavior.
2. **Slice by API boundary, not by file.** Refactor one endpoint/package at a time, verify independently, merge.
3. **Use a strangler pattern.** Route one endpoint at a time through new code path. Old + new coexist until migration complete.
4. **Track with a spreadsheet, not memory.** Column per package/endpoint: "not started / in progress / merged / verified in production."
5. **Every slice is independently revertible.** If slice 3 causes a regression, revert only slice 3 — slices 1 and 2 stay.

### Dependency Upgrade Refactoring

1. **Read the changelog thoroughly.** Breaking changes are usually documented. Don't discover them in production.
2. **Search codebase for deprecated usage.** `grep` for the deprecated functions/APIs listed in the changelog before upgrading.
3. **One major version at a time.** Don't jump from v1 → v4. Each major version may require different migration steps.
4. **Run tests after each version bump.** Not just at the end. A failure after bumping v1→v2 tells you exactly where the break is.
5. **Codmods when available.** React, Angular, NestJS provide migration codemods. Use them — they catch edge cases you'll miss manually.
- Replace string concatenation in loops with `strings.Builder`

## Phase 3 — Verify

After each refactoring (or batch of related refactorings):

1. **Run existing tests.** If the project has tests: `npm test`, `pytest`, `go test ./...`, etc. All must pass.
2. **Type check.** `tsc --noEmit`, `mypy`, etc. No new errors.
3. **Lint.** `eslint`, `ruff check`, `golangci-lint`. No new violations.
4. **If no tests exist:** state clearly "This project has no tests — refactoring is higher risk. Here's what I changed and why it should behave identically."

**If anything fails:** STOP. Identify what broke. Fix it before continuing. Never leave a refactoring half-done with failing tests.

## Phase 4 — Summary

Report comprehensive summary:

```
## Refactoring Summary

**Scope:** N files (list paths)
**Changes:**
  - Extracted X methods
  - Removed Y dead code blocks
  - Renamed Z symbols for consistency
  - Simplified N nested conditions
  - Removed M duplicated blocks → extracted to shared location

**Tests:** E passing → E passing (no regressions)

**Rollback:** `git checkout -- <files>` or `git reset --hard HEAD~1` if committed
```

---

## Guard Rails

- **Never change behavior during refactoring.** If the user wants a behavior change, they'll ask for it separately.
- **Never skip tests.** If tests exist and you don't run them, you're gambling.
- **Never refactor and add features in the same change.** One thing at a time.
- **Never delete tests.** Even if they test "implementation details" — that's a separate discussion.
- **Never leave commented-out code behind.** Delete it. Git history preserves it.
- **Don't introduce abstractions for hypothetical futures.** YAGNI. Extract only when there's actual duplication or the function is too long *right now*.
- **Don't rename across the codebase without checking all references.** Use Grep to find every call site before renaming.
- **Don't restructure working code without a concrete benefit.** "I think this is cleaner" is not enough. "This 87-line function should be 3 functions so each can be tested independently" is.
- **When in doubt, smaller change.** A 5-line cleanup that's clearly correct beats a 50-line restructure that needs explanation.

## If You Get Stuck

```
STATUS: BLOCKED
WHY: [one sentence — e.g., "Refactoring this function would break 3 callers that rely on its side effect"]
TRIED: [what was attempted]
NEXT: [what would unblock — "Need to understand if the side effect is intentional or accidental"]
```

Don't force a refactoring that doesn't fit. Suggest an alternative approach or a smaller scope.

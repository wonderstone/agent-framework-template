---
name: code-testing
description: >-
  Test quality and strategy advisor. Covers test pyramid/trophy selection,
  mock vs stub vs fake decision framework, test smell detection (flaky tests,
  implementation-detail tests, over-mocking), mutation testing integration,
  contract testing for microservices, snapshot testing discipline, and
  test generation from specifications. Use when writing tests, reviewing test
  quality, debugging flaky tests, choosing test strategies, or setting up
  testing infrastructure for a project.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Edit
user-invocable: true
---

# Code Testing — Test Quality & Strategy

You improve test quality, not just test quantity. Coverage numbers mean nothing if the tests don't catch bugs. You help write tests that are fast, reliable, and survive refactoring.

## When to Activate

- Writing tests for a new feature or bug fix
- Reviewing existing tests for quality
- Debugging flaky tests (pass sometimes, fail sometimes)
- Choosing between test types (unit vs integration vs E2E)
- Setting up testing infrastructure for a new project
- Evaluating whether test coverage is meaningful or vanity metric
- Designing contract tests between services

---

## §1 — Test Strategy: What to Test Where

### The Testing Trophy (Preferred over Pyramid)

```
           ╱  E2E  ╲          Few: critical user journeys only
          ╱─────────╲
         ╱Integration╲        More: boundaries between modules
        ╱───────────────╲
       ╱   Unit Tests    ╲     Most: pure logic, edge cases
      ╱─────────────────────╲
     ╱   Static Analysis     ╲  Base: types, lint, security scans
```

**Why trophy over pyramid:** Integration tests catch more real bugs per minute of writing than unit tests. The trophy biases toward integration tests for service boundaries and reserves unit tests for pure logic.

### Decision Tree — Which Test Type?

```
What are you testing?

├─ Pure function / algorithm / formatter / parser
│   → Unit test. No I/O, no DB, no network.
│   Example: calculateTax(amount, region) → number

├─ API endpoint / DB query / file I/O
│   → Integration test. Real DB (or testcontainer), real HTTP.
│   Do NOT mock the database.
│   Example: POST /orders → 201 + row in DB

├─ Cross-service boundary (microservices, external APIs)
│   → Contract test. Pact or recorded response (VCR-style).
│   Example: PaymentService.authorize() returns { id, status }

├─ Critical user journey (signup → purchase → receipt)
│   → E2E test. Playwright / Cypress. Real browser.
│   Only 3-5 of these. They're slow and brittle.
│   Example: User buys product, receives email

└─ Visual regression (CSS changes, layout shifts)
    → Snapshot test (components) + visual diff (screenshots)
    Example: Button variant="primary" renders consistently
```

### Mock Policy Decision Tree

```
Does the dependency...
├─ Have a testcontainer / embedded version?
│   → Use the real thing. Never mock what you can run locally.
│   (Postgres, Redis, Kafka all have testcontainers)
│
├─ Belong to another team / external service?
│   → Contract test (Pact) + recorded responses for dev
│
├─ Make the test non-deterministic? (time, random, weather)
│   → Inject a clock/seed interface, stub with fixed values
│
├─ Make the test slow AND you call it 100+ times?
│   → Stub at the outermost boundary, not deep inside
│
└─ Is it the system under test?
    → NEVER mock what you're testing
```

---

## §2 — Unit Testing: Patterns & Anti-Patterns

### Test Structure: AAA Pattern

```typescript
test('returns empty array when no markets match query', () => {
  // Arrange — set up the world
  const repository = new InMemoryMarketRepository([])
  const service = new MarketService(repository)

  // Act — do the thing
  const result = await service.search('nonexistent')

  // Assert — check the outcome
  expect(result).toEqual([])
})
```

### Test Naming Convention

```
PASS: test('[subject] [scenario] → [expected outcome]')
  "returns empty array when no markets match query"
  "throws ValidationError when email is missing @"
  "retries 3 times then throws on persistent network failure"

FAIL:
  "test search"         ← vague
  "works"               ← tells nothing when it fails
  "test_market_service" ← describes code, not behavior
```

### What Makes a Good Unit Test

| Property | Good | Bad |
|---|---|---|
| **Fast** | <10ms | >100ms (has I/O hidden inside) |
| **Deterministic** | Same result every run | Flaky — fails 1 in 10 runs |
| **Isolated** | Can run alone, in any order | Depends on global state from previous test |
| **Behavioral** | Asserts what the code DOES | Asserts HOW the code does it (implementation detail) |
| **Resilient** | Survives refactoring | Breaks when you rename a variable |

### Test Anti-Patterns

#### Anti-Pattern 1: Testing Implementation Details

```typescript
// BAD: Testing internal state
test('increments counter variable', () => {
  const component = render(<Counter />)
  const button = component.getByRole('button')
  fireEvent.click(button)
  expect(component.state.count).toBe(1)  // ← testing internal state
})

// GOOD: Testing observable behavior
test('displays incremented count when clicked', () => {
  render(<Counter />)
  fireEvent.click(screen.getByRole('button'))
  expect(screen.getByText('Count: 1')).toBeVisible()  // ← testing what user sees
})
```

#### Anti-Pattern 2: Over-Mocking

```typescript
// BAD: Mocking everything — test passes but proves nothing real
const mockDb = { query: jest.fn().mockResolvedValue([{ id: 1 }]) }
const mockEmail = { send: jest.fn() }
const mockQueue = { add: jest.fn() }
// ... 10 more mocks ...
// Test: "works" — but does it? DB could have changed schema.

// GOOD: Use real DB, stub only external boundaries
const db = await createTestDatabase()  // real Postgres in testcontainer
const emailStub = new InMemoryEmailService()  // only boundary is stubbed
```

#### Anti-Pattern 3: Assertion-Free Tests

```typescript
// BAD: Test that never fails
test('processes order', async () => {
  await service.processOrder(order)  // no assertion — test always passes
})

// GOOD: Assert the outcome
test('marks order as paid after successful payment', async () => {
  await service.processOrder(order)
  const saved = await db.orders.findById(order.id)
  expect(saved.status).toBe('paid')
})
```

#### Anti-Pattern 4: Testing Framework, Not Code

```typescript
// BAD: Testing that React works
test('useState updates value', () => {
  const { result } = renderHook(() => useState(0))
  act(() => result.current[1](5))
  expect(result.current[0]).toBe(5)  // ← testing React, not your code
})
```

#### Anti-Pattern 5: Shared Mutable State Between Tests

```typescript
// BAD: Tests depend on each other
let sharedUser: User
test('creates user', async () => {
  sharedUser = await createUser({ name: 'Alice' })  // ← mutating shared state
})
test('updates user', async () => {
  await updateUser(sharedUser.id, { name: 'Bob' })  // ← depends on previous test
})

// GOOD: Each test creates its own state
test('creates user', async () => {
  const user = await createUser({ name: 'Alice' })
  expect(user.name).toBe('Alice')
})
test('updates user', async () => {
  const user = await createUser({ name: 'Pre-existing' })
  await updateUser(user.id, { name: 'Bob' })
  expect((await getUser(user.id)).name).toBe('Bob')
})
```

---

## §3 — Integration Testing

### What to Integration-Test

Integration tests shine at **module boundaries**: API → DB, Service → Queue, HTTP → Auth middleware. Test the contract between two real components, not the internal logic of either.

```typescript
// Integration test: real HTTP handler → real database
test('POST /orders creates order and returns 201', async () => {
  // Use testcontainer or in-memory DB that matches production schema
  const db = await createTestDatabase()
  await migrate(db)

  const server = createServer({ db })

  const response = await server.post('/api/orders', {
    body: { productId: 'p1', quantity: 2 }
  })

  expect(response.status).toBe(201)
  expect(response.body.data.id).toBeDefined()

  // Verify side effect — the row actually exists
  const row = await db.query('SELECT * FROM orders WHERE id = $1', [response.body.data.id])
  expect(row.quantity).toBe(2)
})
```

### Database Testing Rules

1. **Use a real database.** Testcontainers (Postgres, MySQL) or SQLite with same dialect. Mocking `db.query()` is the #1 cause of false-positive tests.
2. **Migrate before tests.** Run the same migrations as production. Schema drift between test and production = worthless tests.
3. **Clean between tests.** Transaction rollback or truncate. Never depend on test execution order.
4. **Seed minimal data.** Only what the test needs. Helper factories, not giant fixture files.

### Test Fixture Factories (Not Fixture Files)

```typescript
// BAD: Giant JSON fixture file with 50 fields, 48 of which are irrelevant
// GOOD: Factory function with sensible defaults
function createTestUser(overrides: Partial<User> = {}): User {
  return {
    id: randomUUID(),
    email: `test-${randomUUID()}@example.com`,
    name: 'Test User',
    role: 'user',
    ...overrides  // only override what matters for this test
  }
}

// Usage — the test communicates intent through overrides
test('prevents non-admin from deleting users', async () => {
  const user = await createTestUser({ role: 'user' })
  // ...
})
```

---

## §4 — Contract Testing (Microservices)

When two services communicate, integration tests in each service can't tell you if the contract is broken. Contract tests fill this gap.

```typescript
// Provider (Payment Service) — verifies it meets consumer expectations
// Consumer (Order Service) — verifies provider meets its needs

// Consumer-side contract (Order Service)
const pact = new Pact({
  consumer: 'OrderService',
  provider: 'PaymentService'
})

pact.addInteraction({
  uponReceiving: 'a payment authorization request',
  withRequest: {
    method: 'POST',
    path: '/authorize',
    body: { orderId: '123', amountCents: 1999 }
  },
  willRespondWith: {
    status: 200,
    body: { authorizationId: 'auth_abc', status: 'authorized' }
  }
})

// Provider verifies this contract against its real implementation
```

**When to use contract tests:** Only for cross-team or cross-service boundaries. Same-team services can use shared integration tests.

---

## §5 — Snapshot Testing Discipline

Snapshots are powerful but dangerous. Used wrong, they become "update without reading" noise.

### Good Snapshots

```typescript
// Small, focused snapshots of stable output
test('renders error message for invalid email', () => {
  const { container } = render(<EmailInput value="not-an-email" touched={true} />)
  expect(container.firstChild).toMatchSnapshot()
  // Snapshot: a single error message, ~5 lines
})
```

### Bad Snapshots

```typescript
// BAD: Giant snapshots — nobody reads them
test('renders dashboard', () => {
  const { container } = render(<Dashboard data={hugeDataset} />)
  expect(container.firstChild).toMatchSnapshot()
  // Snapshot: 500+ lines. Will be "updated" without review.
})
```

### Snapshot Rules

| Rule | Reason |
|---|---|
| Max 30 lines per snapshot | Beyond that, humans stop reviewing |
| One snapshot per test | Multiple snapshots = multiple blind updates |
| Review snapshot diffs like code | If you don't understand the diff, don't approve |
| Prefer inline assertions for dynamic data | `expect(screen.getByText(user.name)).toBeVisible()` beats snapshot |
| Delete unused snapshots | Stale snapshots teach developers to ignore them |

---

## §6 — Flaky Test Diagnosis

### Flaky Test Decision Tree

```
Test fails inconsistently?

├─ Depends on external service that's sometimes down?
│   → Record responses (VCR/nock/msw). Never hit real external services in CI.
│
├─ Depends on timing? (setTimeout, animation frame, debounce)
│   → Use fake timers: jest.useFakeTimers(), vi.useFakeTimers()
│
├─ Depends on current time / date?
│   → Inject a Clock interface, stub with fixed date in tests
│
├─ Depends on random values without seed?
│   → Pass seed to random generator, or assert on properties not values
│
├─ Depends on test execution order?
│   → Each test is leaking state. Find the leak. Fix isolation.
│
├─ Depends on network latency / concurrency timing?
│   → Race condition in production code. This is a real bug, not a test problem.
│
└─ Fails only in CI, never locally?
    → Check: timezone, locale, Node version, filesystem case-sensitivity
```

### Flaky Test Quarantine

If a flaky test can't be fixed immediately:

1. Quarantine it: move to a separate suite, skip in CI (not delete — you'll forget)
2. Create a ticket with the failure log
3. Fix within the sprint — flaky tests rot fast

Never: delete a failing test. It was written for a reason. Understand the reason first.

---

## §7 — Mutation Testing

Coverage tells you what code was executed. Mutation testing tells you if the tests actually check the result.

```bash
# Stryker (JS/TS)
npx stryker run

# Mutmut (Python)
mutmut run

# PIT (Java)
mvn pitest:mutationCoverage
```

**How it works:** The tool mutates your code (`>` becomes `>=`, `&&` becomes `||`, returns `null` instead of value) and re-runs tests. If tests still pass after mutation, you have a coverage gap.

**Survivors = untested behavior.** A mutation that survives your test suite is code whose behavior no test verifies.

Performance note: mutation testing is slow (minutes to hours). Run it on changed files only, not the whole codebase.

---

## §8 — Test Generation from Specifications

When generating tests from a spec or interface, follow this priority:

1. **Happy path first.** The primary use case. "Given valid input, returns expected output."
2. **Error paths.** Every way the function can fail. Invalid input, missing data, network failure.
3. **Edge cases.** Empty input, max/min values, boundary conditions, 0, null, undefined.
4. **Invariants.** Properties that must always hold. "Sorting a list twice gives the same result as sorting once."

```typescript
// Specification: parsePage(page: string): number
//   Parses a page query parameter (1-indexed).
//   Throws if page < 1, is not a number, or is not an integer.

// Generated tests — one per behavior:
test('parses "1" as 1', () => expect(parsePage('1')).toBe(1))
test('parses "42" as 42', () => expect(parsePage('42')).toBe(42))
test('throws on "0" (pages are 1-indexed)', () => expect(() => parsePage('0')).toThrow())
test('throws on "-1"', () => expect(() => parsePage('-1')).toThrow())
test('throws on "abc"', () => expect(() => parsePage('abc')).toThrow())
test('throws on "1.5" (not an integer)', () => expect(() => parsePage('1.5')).toThrow())
test('throws on empty string', () => expect(() => parsePage('')).toThrow())
```

---

## Guard Rails

- **Never mock what you don't own without a contract test.** Mocking a third-party API? Also write a contract test against the real API.
- **Never delete a failing test without understanding why it was written.** Quarantine it, investigate, then decide.
- **Never skip tests in CI.** Skipped tests are dead tests. Fix or delete.
- **Don't write tests for framework code.** Don't test that React renders, Express routes, or Prisma queries — those have their own tests.
- **Don't aim for 100% coverage.** Aim for meaningful coverage on critical paths. 80% coverage with high mutation score > 100% coverage with low mutation score.
- **Speed matters.** A test suite that takes 30 minutes stops being run before commits.
- **Test behavior, not implementation.** If refactoring (same behavior, different code) breaks tests, the tests are wrong.

## Verification

After writing or modifying tests:
1. Run the specific test — verify it passes
2. Break the production code intentionally — verify the test catches it
3. Run the full suite — verify no regressions
4. Run mutation testing on the changed module — check for survivors

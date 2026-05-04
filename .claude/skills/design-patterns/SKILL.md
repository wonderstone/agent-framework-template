---
name: design-patterns
description: >-
  Design pattern catalog and advisor covering architecture patterns (Hexagonal,
  Clean, DDD, CQRS), backend patterns (Repository, Service, Middleware, Caching,
  Queue, Retry), frontend patterns (Composition, Compound, Render Props, Hooks,
  State Management), API design (REST conventions, pagination, versioning, error
  formats), and language-specific idioms (TS, Python, Go, Java). Use when designing
  new features, refactoring architecture, choosing between pattern alternatives,
  or reviewing code for pattern violations.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
user-invocable: true
---

# Design Patterns — Architecture & Implementation Advisor

You are a design pattern advisor. You help choose the right pattern for the right problem, apply it correctly, and recognize when a pattern is being misused. You operate across architecture, backend, frontend, API, and language-specific levels.

## When to Activate

- Designing new features or modules from scratch
- Choosing between architectural approaches (layered vs hexagonal vs CQRS)
- Refactoring tightly coupled code toward cleaner boundaries
- Reviewing code for pattern violations or anti-patterns
- Planning API contracts (REST, GraphQL, RPC)
- Structuring component hierarchies in frontend code
- Applying language-specific idioms correctly

## Decision Tree — Which Pattern Level?

```
User needs help with...
├─ System architecture / module boundaries / dependency direction
│   → Architecture Patterns (§1)
├─ Server-side logic / data access / API structure / caching / jobs
│   → Backend Patterns (§2)
├─ UI component design / state management / performance
│   → Frontend Patterns (§3)
├─ API contract design / versioning / error handling
│   → API Patterns (§4)
├─ Language- or framework-specific best practices
│   → Language Idioms (§5)
└─ Choosing between alternative approaches
    → Pattern Selection Guide (§6)
```

---

## §1 — Architecture Patterns

### 1.1 Hexagonal Architecture (Ports & Adapters)

**When to use:**
- Long-term maintainability and testability matter
- Domain logic is mixed with I/O concerns (refactoring target)
- Supporting multiple interfaces for the same use case (HTTP, CLI, queue, cron)
- Replacing infrastructure (DB, external APIs) without rewriting business rules

**Core rule:** Dependency direction is always inward.
- Adapters → Application/Domain (NEVER the reverse)
- Domain imports nothing external

```
src/features/<feature>/
├── domain/              # Business rules, entities, value objects — NO framework imports
├── application/
│   ├── ports/
│   │   ├── inbound/     # What the app CAN do (use-case interfaces)
│   │   └── outbound/    # What the app NEEDS (repository, gateway, logger ports)
│   └── use-cases/       # Orchestrates domain, receives ports via constructor
├── adapters/
│   ├── inbound/         # HTTP controllers, CLI handlers, queue consumers
│   └── outbound/        # DB repositories, API clients, SDK wrappers
└── composition/         # Single wiring location — binds adapters to use cases
```

**TypeScript example:**

```typescript
// Outbound port (application layer)
export interface OrderRepositoryPort {
  save(order: Order): Promise<void>
  findById(orderId: string): Promise<Order | null>
}

// Use case (application layer)
export class CreateOrderUseCase {
  constructor(private readonly orderRepo: OrderRepositoryPort) {}

  async execute(input: CreateOrderInput): Promise<CreateOrderOutput> {
    const order = Order.create(input)
    await this.orderRepo.save(order)
    return { orderId: order.id }
  }
}

// Outbound adapter (infrastructure layer)
export class PostgresOrderRepository implements OrderRepositoryPort {
  constructor(private readonly db: SqlClient) {}

  async save(order: Order): Promise<void> {
    await this.db.query(
      'INSERT INTO orders (id, status) VALUES ($1, $2)',
      [order.id, order.status]
    )
  }
}

// Composition root
export const createOrderUseCase = new CreateOrderUseCase(
  new PostgresOrderRepository(db)
)
```

**Anti-patterns to avoid:**
- Domain entities importing ORM models, web framework types, or SDK clients
- Use cases reading directly from `req`, `res`, or queue metadata
- Returning database rows directly from use cases without mapping
- Adapters calling each other directly (must flow through use-case ports)
- Spreading dependency wiring across hidden global singletons

**Migration playbook (from layered to hexagonal):**
1. Pick one vertical slice (single endpoint) with frequent change pain
2. Extract a use-case boundary with explicit input/output types
3. Introduce outbound ports around existing infrastructure calls
4. Move orchestration from controllers into the use case
5. Keep old adapters, make them delegate to the new use case
6. Add tests around the new boundary
7. Repeat slice-by-slice — never big-bang rewrite

### 1.2 Clean Architecture

Same dependency rule as hexagonal. Terminology differs:
- Entities (domain) → Use Cases (application) → Interface Adapters → Frameworks
- Use when the team already speaks "Clean Architecture" language

### 1.3 CQRS (Command Query Responsibility Segregation)

**When to use:**
- Read and write models diverge significantly
- Complex query requirements (joins, aggregations) that don't fit the write model
- Separate scaling needs for reads vs writes

```
Command side:  POST /api/orders      → Command → Write Model → Event Store
Query side:    GET /api/orders/:id    → Query → Read Model (denormalized)
```

**Don't use CQRS for:** Simple CRUD where read and write models are identical.

### 1.4 Event-Driven Architecture

**When to use:**
- Multiple services need to react to the same business event
- Loose coupling between bounded contexts
- Audit trail and event sourcing required

```
OrderPlaced → [Payment Service, Notification Service, Inventory Service]
```

---

## §2 — Backend Patterns

### 2.1 Repository Pattern

**Purpose:** Abstract data access behind an interface. Domain/application code never touches ORM/DB directly.

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>
  findByEmail(email: string): Promise<User | null>
  save(user: User): Promise<void>
  delete(id: string): Promise<void>
}
```

**When NOT to use:** Simple CRUD with no domain logic — the ORM is already a repository.

### 2.2 Service Layer

**Purpose:** Business logic between controllers and repositories. Controllers handle HTTP; services handle business rules.

```typescript
class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentGateway: PaymentGatewayPort
  ) {}

  async placeOrder(input: PlaceOrderInput): Promise<Order> {
    // 1. Validate business rules
    if (input.amountCents <= 0) throw new BusinessRuleError('Amount must be positive')

    // 2. Orchestrate domain
    const order = Order.create(input)
    const payment = await this.paymentGateway.authorize(order.total)

    // 3. Persist
    order.markPaid(payment.id)
    await this.orderRepo.save(order)

    return order
  }
}
```

### 2.3 Middleware / Chain of Responsibility

**Purpose:** Cross-cutting concerns applied to multiple endpoints (auth, logging, rate limiting, validation).

```typescript
// Composable middleware wrappers
export function withAuth(handler: Handler): Handler {
  return async (req, res) => {
    const user = await authenticate(req)
    if (!user) return res.status(401).json({ error: 'Unauthorized' })
    return handler({ ...req, user }, res)
  }
}

// Usage — higher-order functions compose the chain
export const GET = withAuth(withRateLimit(actualHandler))
```

### 2.4 Cache-Aside Pattern

```typescript
async function getUser(id: string): Promise<User> {
  // 1. Check cache
  const cached = await redis.get(`user:${id}`)
  if (cached) return JSON.parse(cached)

  // 2. Fetch from DB
  const user = await db.user.findUnique({ where: { id } })
  if (!user) throw new NotFoundError('User not found')

  // 3. Populate cache (TTL: 5min)
  await redis.setex(`user:${id}`, 300, JSON.stringify(user))
  return user
}
```

**Invalidation strategy:** Delete cache key on write. Accept eventual consistency.

### 2.5 Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (i === maxRetries - 1) throw error
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000)) // 1s, 2s, 4s
    }
  }
  throw new Error('Unreachable')
}
```

### 2.6 Background Job Queue

For work that doesn't need to complete within the request-response cycle:

```typescript
// Enqueue (non-blocking)
await queue.add('send-welcome-email', { userId: user.id })

// Process (background worker)
queue.process('send-welcome-email', async (job) => {
  const user = await db.user.findUnique({ where: { id: job.data.userId } })
  await emailService.sendWelcome(user.email)
})
```

### 2.7 Error Handling — Centralized + Typed

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string
  ) {
    super(message)
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'not_found', `${resource} not found`)
  }
}

class BusinessRuleError extends AppError {
  constructor(message: string) {
    super(422, 'business_rule_violation', message)
  }
}
```

---

## §3 — Frontend Patterns

### 3.1 Component Composition (Over Inheritance)

React components should compose, never inherit:

```typescript
// Composition — small, focused pieces combined
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter><Button>Action</Button></CardFooter>
</Card>
```

### 3.2 Compound Components

When a group of components share implicit state:

```typescript
<Tabs defaultTab="overview">
  <TabList>
    <Tab id="overview">Overview</Tab>
    <Tab id="details">Details</Tab>
  </TabList>
  <TabPanel id="overview"><Overview /></TabPanel>
  <TabPanel id="details"><Details /></TabPanel>
</Tabs>
```

Pattern: Context provides shared state; children read it. Throw if a child is used outside its parent.

### 3.3 Custom Hooks — Extract Reusable Logic

```typescript
// Data fetching hook
function useQuery<T>(key: string, fetcher: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetcher().then(setData).catch(setError).finally(() => setLoading(false))
  }, [key])

  return { data, error, loading, refetch: () => { /* ... */ } }
}
```

**Hooks should:** Do one thing, be framework-agnostic where possible, have clear input/output types.

### 3.4 State Management — Choose by Complexity

| Complexity | Solution |
|---|---|
| Local UI state | `useState` |
| Shared page state | Lift to parent or Context |
| Complex global state | `useReducer` + Context or Zustand |
| Server state / cache | React Query / SWR (NOT Redux) |
| URL state | `useSearchParams` — source of truth for filters/pagination |

### 3.5 React Server Components (RSC) & Async Patterns (2025+)

Next.js App Router and React 19 changed the component model fundamentally. Know when to use each:

```
Server Component (default in app/)
├─ Async, runs at build/request time on the server
├─ Can directly await DB queries, file reads, fetch
├─ NO interactivity (no useState, useEffect, onClick)
├─ Ships zero JS to client
└─ Use for: data fetching, heavy computation, SEO content

Client Component ('use client' boundary)
├─ Runs in browser, fully interactive
├─ CANNOT directly access DB, filesystem
├─ Can use hooks, event handlers, browser APIs
└─ Use for: forms, buttons, animations, real-time updates
```

**Pattern: Server Component fetches, Client Component hydrates.**

```typescript
// Server Component (app/markets/page.tsx) — async, no 'use client'
export default async function MarketsPage() {
  const markets = await db.market.findMany({ where: { status: 'active' } })
  // This runs on the server. Zero JS sent for this component.
  return <MarketList markets={markets} />
}

// Client Component (components/market-list.tsx) — 'use client' boundary
'use client'
export function MarketList({ markets }: { markets: Market[] }) {
  const [filter, setFilter] = useState('all')
  // Interactive — has state, event handlers
  return (/* render filtered list */)
}
```

**Pattern: Streaming + Suspense for progressive rendering.**

```typescript
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <Header />  {/* renders immediately */}
      <Suspense fallback={<Skeleton />}>
        <SlowChartSection />  {/* streams in when ready — doesn't block page */}
      </Suspense>
    </div>
  )
}
```

**Pattern: Server Actions for mutations (replaces API routes for forms).**

```typescript
// app/actions.ts — Server Action
'use server'
export async function createMarket(formData: FormData) {
  const session = await auth()  // ALWAYS re-authenticate inside
  if (!session) throw new Error('Unauthorized')

  const validated = CreateMarketSchema.parse(Object.fromEntries(formData))
  await db.market.create({ data: validated })
  revalidatePath('/markets')  // refresh the cache
}
```

**RSC decision tree:**

```
Component needs...
├─ Data from DB/API? → Server Component (async, direct fetch)
├─ Interactivity (state, effects, events)? → Client Component
├─ Both data + interactivity? → Server Component fetches, passes to Client Component as props
└─ Loading state for slow section? → <Suspense> boundary with fallback
```

### 3.5 Performance Optimization — Measure First

```typescript
// Memoize expensive computations
const sorted = useMemo(() => items.sort(byVolume), [items])

// Memoize callbacks passed to children
const handleClick = useCallback((id: string) => { /* ... */ }, [])

// Lazy load heavy components
const Chart = lazy(() => import('./Chart'))

// Virtualize long lists (>100 items)
const virtualizer = useVirtualizer({ count, estimateSize, getScrollElement })
```

**Don't optimize prematurely.** Only memoize when profiling shows it helps.

### 3.6 Error Boundaries

```typescript
class ErrorBoundary extends React.Component<Props, { error: Error | null }> {
  state = { error: null }

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  render() {
    if (this.state.error) {
      return <ErrorFallback error={this.state.error} onReset={() => this.setState({ error: null })} />
    }
    return this.props.children
  }
}
```

---

## §4 — API Design Patterns

### 4.1 REST Resource Naming

```
# Resources: plural nouns, kebab-case
GET    /api/v1/users              # List
GET    /api/v1/users/:id          # Single
POST   /api/v1/users              # Create
PUT    /api/v1/users/:id          # Full replace
PATCH  /api/v1/users/:id          # Partial update
DELETE /api/v1/users/:id          # Delete

# Sub-resources
GET    /api/v1/users/:id/orders

# Actions (use sparingly)
POST   /api/v1/orders/:id/cancel
```

### 4.2 HTTP Status Codes

```
200 OK, 201 Created, 204 No Content
400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests
500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable
```

### 4.3 Response Envelope

```json
// Success (single)
{ "data": { "id": "abc", "name": "Alice" } }

// Success (collection)
{
  "data": [...],
  "meta": { "total": 142, "page": 1, "per_page": 20 },
  "links": { "next": "/api/v1/users?page=2" }
}

// Error
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [{ "field": "email", "message": "Invalid email" }]
  }
}
```

### 4.4 Pagination — Cursor-Based (Preferred for Scale)

```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "meta": { "has_next": true, "next_cursor": "eyJpZCI6MTQzfQ" }
}
```

Use offset-based only for small datasets (<10K) or admin dashboards where "jump to page N" is needed.

### 4.5 Filtering, Sorting, Sparse Fields

```
# Filtering
GET /api/v1/orders?status=active&customer_id=abc
GET /api/v1/products?price[gte]=10&price[lte]=100

# Sorting (- prefix = desc)
GET /api/v1/products?sort=-created_at,price

# Sparse fieldsets (reduce payload)
GET /api/v1/users?fields=id,name,email
```

### 4.6 Versioning Strategy

- URL path versioning: `/api/v1/`, `/api/v2/`
- Maintain at most 2 active versions (current + previous)
- Non-breaking changes (new fields, new endpoints) don't need a new version
- Breaking changes (removing/renaming fields, changing types) require a new version
- Announce deprecation with `Sunset` header; return `410 Gone` after sunset date

---

## §5 — Language-Specific Idioms

### TypeScript/JavaScript

- Prefer `const` over `let`; never `var`
- Use `unknown` over `any`; type guards to narrow
- Prefer `interface` for object shapes, `type` for unions/primitives
- Immutable updates: spread `{ ...obj, field: newValue }`, never mutation
- `Promise.all` for independent async work; never sequential `await` chains
- Use Zod for runtime validation at I/O boundaries

### Python

- Composition over inheritance; use protocols (PEP 544) over ABCs
- Dataclasses for value objects; Pydantic for API models
- Context managers for resource lifecycle (`with open(...)`)
- Generators for memory-efficient iteration
- Type hints mandatory on public APIs
- `async/await` with `asyncio.gather` for concurrent I/O

### Go

- Accept interfaces, return structs
- Make the zero value useful (no constructors needed for simple types)
- Small, focused interfaces (1-3 methods)
- Handle errors explicitly; wrap with `fmt.Errorf("context: %w", err)`
- Use `context.Context` for cancellation and timeouts — always first parameter
- Goroutines coordinated with `errgroup` or `sync.WaitGroup`; always know who owns the channel

### Java

- Constructor injection over field injection (@Autowired on fields = anti-pattern)
- Immutable value objects: `record` (Java 16+) or `@Value` (Lombok)
- Repository interfaces in domain, implementations in infrastructure
- Use `Optional` for nullable returns, never for fields or parameters
- Streams for data transformation pipelines

---

## §6 — Pattern Selection Guide

### Architecture: Simple CRUD → Full DDD spectrum

```
Simple CRUD (no domain logic)
  → Direct ORM usage, no repository abstraction needed

Moderate business rules (most apps)
  → Service Layer + Repository Pattern

Complex domain (finance, healthcare, multi-tenant)
  → Hexagonal Architecture + Domain-Driven Design

High read/write asymmetry
  → CQRS + Event Sourcing
```

### API: Choosing the right protocol

```
Standard CRUD + web/mobile clients
  → REST with OpenAPI spec

Complex nested data + mobile clients with bandwidth constraints
  → GraphQL

Real-time bidirectional communication
  → WebSocket (or SSE for server→client only)

Service-to-service internal communication
  → gRPC or message queue
```

### State: Local → Global spectrum

```
Single component only          → useState
Shared between 2-3 siblings    → Lift state to parent
Shared across many components  → Context + useReducer
Server data (cache, refetch)   → React Query / SWR
Complex global + middleware    → Zustand / Jotai
```

---

## §7 — Database Patterns

### 7.1 Index Design

The most leveraged performance decision in any application:

```sql
-- Equality first, then range, then sort
CREATE INDEX idx_orders_lookup ON orders (customer_id, status, created_at DESC);
```

### 7.2 Migration: Expand-Contract

Never make breaking schema changes in one step. Expand first, contract later:

```
Step 1: ADD new_column (backward-compatible, no downtime)
Step 2: DUAL-WRITE to both old and new columns
Step 3: BACKFILL new column from old data (in batches, not one UPDATE)
Step 4: MIGRATE readers to new column
Step 5: DROP old column (after confirming zero readers remain)
```

### 7.3 Connection Pool

```
Pool size = (core_count * 2) / num_services_connecting
Smaller pools with request queues > larger pools with contention
```

### 7.4 N+1 Prevention: Batch Load

```typescript
const ids = parents.map(p => p.childId)
const children = await db.child.findMany({ where: { id: { in: ids } } })
const map = new Map(children.map(c => [c.id, c]))
```

### 7.5 Optimistic Concurrency

```sql
UPDATE orders SET status = 'paid', version = version + 1
WHERE id = $1 AND version = $2;
-- 0 rows updated → conflict → retry
```

### 7.6 Idempotent Receiver

```sql
INSERT INTO processed_events (event_id) VALUES ($1)
ON CONFLICT (event_id) DO NOTHING;
```

---

## §8 — Concurrency & Messaging Patterns

### 8.1 Optimistic Locking (Preferred over Pessimistic)

See §7.5 — version column pattern. No lock held, no deadlock risk, scales horizontally.

### 8.2 Outbox Pattern (Reliable Event Publishing)

```sql
-- Transactionally write business data + event:
BEGIN;
INSERT INTO orders (id, status) VALUES ($1, 'placed');
INSERT INTO outbox (event_id, type, payload) VALUES ($2, 'OrderPlaced', $3);
COMMIT;
-- Outbox poller publishes to queue; ensures at-least-once delivery
```

### 8.3 Idempotent Consumer (At-Least-Once)

```typescript
async function handle(orderPlaced: OrderPlaced) {
  const done = await db.events.findUnique({ where: { id: orderPlaced.id } })
  if (done) return  // already processed — idempotent replay
  await process(orderPlaced)
}
```

### 8.4 Saga (Distributed Transaction)

```
Order placed → Payment authorized → Inventory reserved → Shipment created
     │                │                    │
     └────────────────┴────────────────────┴── any failure → compensating action
```

### 8.5 Actor Model (Single-Writer Entity)

When concurrent writes to the same entity cause lock contention: give each entity its own lightweight actor (goroutine/process) that processes messages serially. No locks needed.

---

## §9 — Observability Patterns

### 9.1 Structured Logging

```typescript
logger.info('Order placed', { orderId, customerId, amountCents, durationMs })
// Never: console.log(`Order ${id} placed`)
```

### 9.2 RED Metrics

```
Rate — requests/second   Errors — failures/second   Duration — p50/p95/p99
Apply to every endpoint, every external call, every queue consumer.
```

### 9.3 Distributed Tracing

Propagate `trace-id` across services via headers. Every log line, every span carries it.

### 9.4 Health Checks

```
/health      → lightweight (DB ping) — for load balancer
/health/ready → all dependencies connected — for K8s readiness probe
```

### 9.5 Alert on Symptoms, Not Causes

```
GOOD: "Checkout latency p95 > 2s"   ← user impact
BAD:  "CPU > 80% on db-3"           ← cause, not symptom
```

---

## Guard Rails

- Don't propose patterns for their own sake — suggest the simplest thing first
- A pattern that doesn't solve a concrete problem IS over-engineering
- Always show code examples in the project's detected language
- Mention alternatives + tradeoffs, not just one "right" way
- When reviewing: distinguish "this violates the pattern" from "I would have chosen a different pattern"
- Legacy code migration: strangler approach (slice by slice), never big-bang rewrite

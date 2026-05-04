---
name: db-engineering
description: >-
  Database engineering and query optimization advisor. Covers schema design
  (normalization vs denormalization, soft deletes, temporal data), indexing
  strategy (composite column order, covering indexes, partial indexes, index
 -only scans), migration safety (expand-contract, lock-free large tables,
  backward compatibility), query optimization (N+1 detection, query plan
  analysis, slow query diagnosis), connection pooling, transaction isolation
  levels, and ORM best practices across PostgreSQL, MySQL, and SQLite. Use when
  designing schemas, optimizing queries, planning migrations, reviewing data
  access patterns, or debugging database performance issues.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Edit
user-invocable: true
---

# Database Engineering — Schema, Query & Migration Quality

You improve database design, query performance, and migration safety. You don't just write SQL that works — you write SQL that scales, migrates safely, and doesn't surprise oncall at 3 AM.

## When to Activate

- Designing new tables or changing existing schemas
- Debugging slow queries or N+1 problems
- Planning database migrations for large tables
- Reviewing ORM usage for performance pitfalls
- Choosing indexes or analyzing query plans
- Setting up connection pooling or replication
- Evaluating transaction isolation requirements

---

## §1 — Schema Design

### 1.1 Normalization vs Denormalization

```
Normalize when:                    Denormalize when:
├─ Data integrity is critical      ├─ Read performance dominates
├─ Write-heavy workload            ├─ Read-heavy workload
├─ Complex business rules          ├─ Reporting/analytics queries
├─ Many relationships              ├─ Data changes infrequently
└─ Team size > 1 (consistency)     └─ Query involves 5+ joins every time
```

**Rule of thumb:** Start normalized (3NF). Denormalize only when you've measured a performance problem and can point to a specific query.

### 1.2 Column Types — Choose Correctly

```sql
-- BAD: Everything is VARCHAR or TEXT
name VARCHAR(255),
status VARCHAR(20),    -- 'active', 'pending', 'cancelled' — but no constraint
amount VARCHAR(50),    -- '$19.99' — stored as string
created_at VARCHAR(30) -- '2026-05-04' — string comparison, not temporal

-- GOOD: Right type for the job
name TEXT,                 -- PostgreSQL: TEXT is fine, no performance penalty
status order_status,       -- ENUM type: type-safe, space-efficient
amount_cents INTEGER,      -- Money in cents: no floating-point rounding
created_at TIMESTAMPTZ     -- Timezone-aware, comparable, indexable
```

**Type selection rules:**
- Money → `INTEGER` (cents) or `NUMERIC(19,4)`. Never `FLOAT`/`DOUBLE`.
- Timestamps → `TIMESTAMPTZ` (PostgreSQL) or `DATETIME` (MySQL). Always store UTC.
- IDs → `UUID` (random for security, v7 for sortability) or `BIGINT`. Never `INT` for new tables.
- Booleans → `BOOLEAN`. Never `TINYINT(1)` or `CHAR(1)`.
- Enums → Native `ENUM` type or lookup table. Never free-text `VARCHAR` without constraint.

### 1.3 Soft Deletes

```sql
-- Pattern: deleted_at column + filtered index
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  deleted_at TIMESTAMPTZ  -- NULL = active, non-NULL = deleted
);

-- Index that only covers active rows (smaller, faster)
CREATE UNIQUE INDEX idx_users_email_active
  ON users (email) WHERE deleted_at IS NULL;

-- Every query filters out deleted rows
SELECT * FROM users WHERE id = $1 AND deleted_at IS NULL;
```

**Pros:** Recoverable, audit-friendly. **Cons:** Every query must filter. Uniqueness gets complex. Use a view or ORM scope to enforce the `deleted_at IS NULL` filter.

**When NOT to use soft deletes:** High-volume append-only tables (logs, events), GDPR-triggered deletion (must actually delete), tables where deleted rows outnumber active 100:1.

### 1.4 Temporal / Point-in-Time Data

```sql
-- Slowly Changing Dimension Type 2: track history with date ranges
CREATE TABLE product_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id),
  price_cents INTEGER NOT NULL,
  valid_from TIMESTAMPTZ NOT NULL,
  valid_until TIMESTAMPTZ,  -- NULL = currently active
  EXCLUDE USING gist (
    product_id WITH =,
    tstzrange(valid_from, valid_until, '[)') WITH &&
  )  -- prevents overlapping date ranges for same product
);

-- Query: "what was the price on May 1st?"
SELECT price_cents FROM product_prices
WHERE product_id = $1
  AND valid_from <= '2026-05-01'::timestamptz
  AND (valid_until IS NULL OR valid_until > '2026-05-01'::timestamptz);
```

---

## §2 — Indexing Strategy

### 2.1 When to Index

```
Index when:
├─ Column appears in WHERE clauses frequently
├─ Column appears in JOIN conditions
├─ Column appears in ORDER BY with large datasets
├─ You need a UNIQUE constraint
├─ Full-text search (GIN/GiST index)
└─ Covering index can replace table access

Don't index when:
├─ Table has <1000 rows (seq scan is faster)
├─ Column has low cardinality (<5 distinct values, unless combined in composite)
├─ Table is write-heavy and index is never queried
├─ Index would be larger than the table
└─ "Just in case" — measure first
```

### 2.2 Composite Index Column Order

The most common indexing mistake:

```sql
-- Query:
SELECT * FROM orders
WHERE status = 'active' AND customer_id = $1
ORDER BY created_at DESC;

-- BAD index: wrong column order
CREATE INDEX idx_orders_wrong ON orders (status, customer_id, created_at);
-- status has low cardinality (3 values) → first column filters little

-- GOOD index: equality first, then range/order
CREATE INDEX idx_orders_good ON orders (customer_id, status, created_at DESC);
-- customer_id has high cardinality → narrows quickly → then status → then order
```

**Rule for column order:**
1. Equality columns first (`=`, `IN`)
2. Range/comparison columns next (`>`, `<`, `BETWEEN`)
3. `ORDER BY` / `GROUP BY` columns last
4. Highest cardinality equality column goes first

### 2.3 Covering Indexes (Index-Only Scans)

```sql
-- Query only needs id, status, created_at
SELECT id, status, created_at FROM orders WHERE customer_id = $1;

-- Covering index: all queried columns in the index
CREATE INDEX idx_orders_covering ON orders (customer_id) INCLUDE (status, created_at);
-- PostgreSQL can answer entirely from the index — no table access needed
```

### 2.4 Partial Indexes

```sql
-- Only index active orders (5% of table) — much smaller, faster
CREATE INDEX idx_active_orders ON orders (customer_id)
  WHERE status = 'active';

-- Only index unread notifications (typically <1% of table)
CREATE INDEX idx_unread_notifications ON notifications (user_id)
  WHERE read_at IS NULL;
```

### 2.5 Index Health Checks

```sql
-- PostgreSQL: find unused indexes (candidates for removal)
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- PostgreSQL: find duplicate indexes
SELECT array_agg(indexname) AS indexes, tablename, indexdef
FROM pg_indexes
GROUP BY tablename, indexdef
HAVING count(*) > 1;

-- PostgreSQL: find missing indexes (sequential scans on large tables)
SELECT schemaname, tablename, seq_scan, seq_tup_read,
       seq_tup_read / seq_scan AS avg_tup_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0 AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
```

---

## §3 — Query Optimization

### 3.1 N+1 Detection & Fix

```typescript
// BAD: N+1 — 1 query for orders + N queries for customers
const orders = await db.orders.findMany({ where: { status: 'active' } })
for (const order of orders) {
  order.customer = await db.customers.findUnique({ where: { id: order.customerId } })
}
// 101 queries for 100 orders

// GOOD: Eager load — 1 query with JOIN, or 2 queries with batch
const orders = await db.orders.findMany({
  where: { status: 'active' },
  include: { customer: true }  // Prisma: single query with JOIN
})

// Also GOOD: Batch load (DataLoader pattern)
const customerIds = orders.map(o => o.customerId)
const customers = await db.customers.findMany({
  where: { id: { in: customerIds } }
})
const customerMap = new Map(customers.map(c => [c.id, c]))
orders.forEach(o => { o.customer = customerMap.get(o.customerId) })
// 2 queries total
```

**N+1 detection commands:**
```sql
-- PostgreSQL: enable query logging for analysis
SET log_min_duration_statement = 100;  -- log queries >100ms
-- Then look for repeated identical queries with different params
```

### 3.2 Query Plan Analysis

```sql
-- Always use EXPLAIN ANALYZE (not just EXPLAIN) — shows actual times
EXPLAIN ANALYZE
SELECT * FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE orders.status = 'active' AND orders.created_at > now() - interval '30 days';

-- Key metrics to read:
-- "actual time=0.123..45.678" → first row in 0.1ms, all rows in 45ms
-- "rows=5000" → estimated rows (compare to "actual rows")
-- "Seq Scan" on large table → missing index
-- "Index Scan" → using index (good)
-- "Index Only Scan" → covering index (best for reads)
-- "Bitmap Heap Scan" → multiple index scans combined
-- "Nested Loop" → join strategy (fine for small inner table, bad for large)
-- "Hash Join" → hash table in memory (good for large tables, uses memory)
-- "Merge Join" → both inputs sorted (good when ORDER BY matches index)

-- Red flags:
-- "actual rows" much larger than "rows" → stale statistics → run ANALYZE
-- "Seq Scan" on table with >10K rows in a frequent query → add index
-- "Nested Loop" with large row counts → convert to Hash Join
```

### 3.3 Slow Query Checklist

1. Run `EXPLAIN ANALYZE` — where is time actually spent?
2. Check for sequential scans on large tables → missing index
3. Check `rows` vs `actual rows` mismatch → `ANALYZE table_name`
4. Check for repeated similar queries → N+1 in application code
5. Check JOIN order and strategy → sometimes rearranging JOINs helps
6. Check for `ORDER BY` + `LIMIT` without matching index → full sort
7. Check `OFFSET` with large value → switch to cursor-based pagination
8. Check for `SELECT *` → only select needed columns
9. Check for function calls in WHERE that prevent index usage (`WHERE LOWER(email) = ...`)

### 3.4 Common ORM Performance Pitfalls

```typescript
// BAD: SELECT * — fetches all columns including large JSONB/text
const users = await db.user.findMany()  // all 30 columns, including bio TEXT

// GOOD: select only needed columns
const users = await db.user.findMany({
  select: { id: true, email: true, name: true }
})

// BAD: Implicit transaction around every operation
for (const item of items) {
  await db.orderItem.create({ data: item })  // each is a separate transaction
}

// GOOD: Batch create in a single transaction
await db.$transaction(
  items.map(item => db.orderItem.create({ data: item }))
)

// BAD: Loading relations one by one (hidden N+1)
const posts = await db.post.findMany()
// Later in template: post.author.name — triggers N queries

// GOOD: Explicit eager loading
const posts = await db.post.findMany({ include: { author: true } })
```

---

## §4 — Migration Safety

### 4.1 The Expand-Contract Pattern

Never make a breaking schema change in one migration. Always expand first, then contract.

```
Step 1: EXPAND — add new column/table (backward-compatible, no downtime)
  ALTER TABLE users ADD COLUMN full_name TEXT;

Step 2: DUAL-WRITE — application writes to both old and new
  INSERT INTO users (name, full_name) VALUES ($1, $2)

Step 3: BACKFILL — populate new column from old data
  UPDATE users SET full_name = name WHERE full_name IS NULL

Step 4: MIGRATE READS — switch readers to new column
  SELECT full_name FROM users

Step 5: CONTRACT — remove old column (after confirming no readers remain)
  ALTER TABLE users DROP COLUMN name;
```

### 4.2 Safe Operations on Large Tables

```sql
-- DANGEROUS: locks table for duration (blocks all writes)
ALTER TABLE orders ADD COLUMN metadata JSONB DEFAULT '{}'::jsonb;

-- SAFE: add nullable column first, then set default later
-- Step 1: Add nullable (instant in PostgreSQL 11+)
ALTER TABLE orders ADD COLUMN metadata JSONB;

-- Step 2: Set default for new rows (instant)
ALTER TABLE orders ALTER COLUMN metadata SET DEFAULT '{}'::jsonb;

-- Step 3: Backfill existing rows in batches (no long lock)
UPDATE orders SET metadata = '{}'::jsonb
WHERE id IN (SELECT id FROM orders WHERE metadata IS NULL LIMIT 1000);
-- Repeat until 0 rows updated

-- DANGEROUS: adding NOT NULL with validation
ALTER TABLE orders ALTER COLUMN metadata SET NOT NULL;

-- SAFE: add NOT NULL as "not valid" first, then validate
ALTER TABLE orders ADD CONSTRAINT metadata_not_null CHECK (metadata IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT metadata_not_null;
-- VALIDATE takes a brief SHARE UPDATE EXCLUSIVE lock — doesn't block reads/writes
```

### 4.3 Migration Checklist

Before every migration:

- [ ] Does `ADD COLUMN` need a default? Use `ADD` → `SET DEFAULT` → backfill pattern for large tables
- [ ] Does `DROP COLUMN` have application code still reading it? Grep first.
- [ ] Does index creation use `CONCURRENTLY`? (PostgreSQL — avoids locking writes)
- [ ] Does `RENAME COLUMN` have ORM references that won't update automatically?
- [ ] Is the migration reversible? If not, document the rollback plan.
- [ ] Tested on a staging database with production-like data volume?
- [ ] For adding NOT NULL: use `NOT VALID` → `VALIDATE` pattern
- [ ] For changing column type: use `USING` clause or intermediate column

### 4.4 Rollback Strategy

```sql
-- Every migration file should have a corresponding down migration
-- Up (20260504120000_add_user_full_name.sql):
ALTER TABLE users ADD COLUMN full_name TEXT;
UPDATE users SET full_name = name;

-- Down (rollback):
ALTER TABLE users DROP COLUMN full_name;
```

If a migration can't be cleanly rolled back (e.g., `DROP COLUMN`), document the restore-from-backup procedure.

---

## §5 — Connection Management & Transaction Isolation

### 5.1 Connection Pool Sizing

```
Pool size = (core_count * 2) / number_of_services_connecting

PostgreSQL: each connection = ~10MB + one backend process.
MySQL: each connection = ~4MB + one thread.

For a 4-core DB server with 3 app instances:
  Pool per app = (4 * 2) / 3 = 2-3 connections maximum
  Total = 9 connections (well within PostgreSQL default of 100)
```

**Rule:** Smaller pools with queues beat larger pools. Too many connections → context switching kills throughput.

### 5.2 Transaction Isolation Guide

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Use When |
|-------|-----------|-------------------|-------------|----------|
| Read Uncommitted | Yes | Yes | Yes | Almost never |
| Read Committed | No | Yes | Yes | PostgreSQL default — fine for most things |
| Repeatable Read | No | No | Yes* | Financial calculations, reports |
| Serializable | No | No | No | Payment processing, inventory |

*PostgreSQL Repeatable Read actually prevents phantoms (stronger than SQL standard).

### 5.3 Transaction Pitfalls

```typescript
// BAD: Long-running transaction — holds locks, blocks vacuum
await db.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } })
  await externalApi.sendEmail(user.email)  // ← network I/O inside transaction!
  await tx.auditLog.create({ data: { action: 'email_sent' } })
  // Transaction held open for 500ms+ waiting for external API
})

// GOOD: External calls outside transaction
const user = await db.user.findUnique({ where: { id } })
await externalApi.sendEmail(user.email)  // I/O outside transaction
await db.$transaction(async (tx) => {
  await tx.auditLog.create({ data: { action: 'email_sent' } })
  // Transaction held for <5ms
})
```

### 5.4 Optimistic Concurrency

```sql
-- Instead of pessimistic locking (SELECT FOR UPDATE):
-- Use a version column for optimistic locking

-- Schema:
ALTER TABLE orders ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Update with version check:
UPDATE orders
SET status = 'paid', version = version + 1
WHERE id = $1 AND version = $2;
-- If rows_affected = 0 → someone else modified it → retry or conflict
```

---

## §6 — Database-Specific Best Practices

### PostgreSQL

```sql
-- Use BRIN indexes for append-only time-series tables (huge tables, small index)
CREATE INDEX idx_events_time ON events USING BRIN (created_at)
  WITH (pages_per_range = 32);

-- Use GIN for full-text search or array containment
CREATE INDEX idx_products_search ON products USING GIN (to_tsvector('english', name || ' ' || description));

-- Partition large tables by date range
CREATE TABLE orders (
  id UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2026_01 PARTITION OF orders FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Regular maintenance
VACUUM ANALYZE;  -- reclaim space + update statistics
REINDEX INDEX CONCURRENTLY idx_name;  -- rebuild bloated index without locking
```

### MySQL

```sql
-- InnoDB: always use a PRIMARY KEY (clustered index)
-- UUIDs fragment the clustered index → use ULID or AUTO_INCREMENT for PK
-- Use EXPLAIN FORMAT=JSON for detailed query plan
EXPLAIN FORMAT=JSON SELECT * FROM orders WHERE customer_id = 1;

-- Check slow query log
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 0.1;  -- log queries >100ms
```

### SQLite

```sql
-- Single-writer design: use WAL mode for concurrent reads
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;

-- Only one writer at a time — batch writes into transactions
BEGIN;
INSERT INTO orders VALUES (...);
INSERT INTO order_items VALUES (...);
COMMIT;  -- 100x faster than individual inserts
```

---

## §7 — ORM Best Practices

### When to Use Raw SQL vs ORM

```
Use ORM for:                       Use raw SQL for:
├─ Simple CRUD                    ├─ Complex reporting queries
├─ Migrations                     ├─ Bulk operations (>10K rows)
├─ Type-safe queries              ├─ Performance-critical paths
├─ Prototyping                    ├─ Database-specific features (window functions, CTEs, lateral joins)
└─ 90% of application code        └─ The 10% where ORM generates bad SQL
```

**Rule:** Know the SQL your ORM generates. Run `prisma:query` logging or `typeorm` logging in development. If the generated SQL surprises you, that's a problem.

---

## Guard Rails

- **Never run a migration against production without testing on staging first.** With production-like data volume.
- **Never use `SELECT *` in production code.** Only select columns you need. Schema changes shouldn't break unrelated queries.
- **Never store money as float.** `INTEGER` (cents) or `NUMERIC(19,4)`.
- **Never run queries inside loops without batching.** N+1 is the most common production outage cause.
- **Never hold a transaction open across network I/O.** External API calls, email sending, queue publishing — all outside the transaction.
- **Never add a unique index without handling the conflict path.** Duplicate key errors will happen.
- **Always use parameterized queries.** Never concatenate user input into SQL strings.
- **Always set a statement timeout** in production: `SET statement_timeout = '30s'`.

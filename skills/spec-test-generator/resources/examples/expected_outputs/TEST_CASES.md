# Test Cases

### TEST-0001 (Unit, P0) — Missing auth returns 401 with error envelope
**Requirements:** REQ-0001, REQ-0004
**Preconditions:** None
**Steps:**
1. Call `GET /users` without Authorization header.
**Expected:**
- Status 401
- Body contains `code`, `message`, `requestId`

### TEST-0002 (Integration, P0) — List users returns items and nextCursor
**Requirements:** REQ-0002, REQ-0003
**Preconditions:** Valid token; directory seeded with users
**Steps:**
1. Call `GET /users?limit=10`
**Expected:**
- Status 200
- Body has `items` array of users with `id,email,displayName`
- Body has `nextCursor` (string, possibly empty if last page)

### TEST-0003 (Unit, P0) — limit > 200 returns 400
**Requirements:** REQ-0002, REQ-0004
**Preconditions:** Valid token
**Steps:**
1. Call `GET /users?limit=500`
**Expected:**
- Status 400
- Standard error envelope includes `requestId`

### TEST-0004 (E2E, P1) — Performance smoke for typical list call
**Requirements:** REQ-0005
**Preconditions:** Perf env; representative dataset
**Steps:**
1. Run 1-5 minutes of load at expected RPS.
**Expected:**
- p95 latency <= 300ms for `GET /users`

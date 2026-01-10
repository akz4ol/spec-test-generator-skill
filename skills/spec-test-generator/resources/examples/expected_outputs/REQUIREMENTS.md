# Requirements

## Assumptions
- This API is internal-only and consumed by trusted admin tools.
- Authentication uses bearer tokens (exact issuer/validation TBD).

## Open Questions
- What is the auth provider / token validation mechanism?
- Is email always present, or can it be null for some users?

## Feature: List Users

### REQ-0001 (P0) — Authenticated access required
**Statement:** The API SHALL require authentication for all endpoints.
**Acceptance Criteria:**
- Given a request without credentials, when calling `GET /users`, then the API returns `401` with standard error envelope.
- Given a request with invalid credentials, when calling `GET /users`, then the API returns `401` with standard error envelope.

**Edge Cases:**
- Expired token.
- Token missing required role/claim (if authorization is added later).

### REQ-0002 (P0) — Cursor pagination for listing users
**Statement:** The API SHALL support cursor pagination on `GET /users` using `limit` and `cursor`.
**Acceptance Criteria:**
- Given no cursor, when calling `GET /users?limit=N`, then response includes `items` and `nextCursor`.
- Given `cursor` from a prior response, when calling `GET /users?cursor=X&limit=N`, then API returns the next page.
- Given `limit` > 200, then API returns `400` with standard error envelope.

**Edge Cases:**
- Invalid cursor format.
- Empty result set.

### REQ-0003 (P0) — User object schema
**Statement:** The API SHALL return each user with fields `id`, `email`, and `displayName`.
**Acceptance Criteria:**
- Each `items[]` entry includes `id` and `email`.
- `displayName` may be empty string but must be present.

**Edge Cases:**
- Missing display name from upstream directory -> return empty string.
- Email format validation errors in source data -> return as-is but log warning (implementation note).

### REQ-0004 (P1) — Consistent error envelope with request ID
**Statement:** Error responses SHALL use a consistent envelope including `code`, `message`, and `requestId`.
**Acceptance Criteria:**
- Given a validation error, when responding with `400`, then body includes `code`, `message`, and `requestId`.
- Given unauthorized, when responding with `401`, then body includes `code`, `message`, and `requestId`.

**Edge Cases:**
- Missing request ID header on input -> server generates one.

## Non-Functional Requirements

### REQ-0005 (P1) — Performance
**Statement:** The API SHOULD achieve p95 latency under 300ms for typical `GET /users` requests.
**Acceptance Criteria:**
- With representative dataset and typical load, p95 <= 300ms for `GET /users` in staging/perf environment.

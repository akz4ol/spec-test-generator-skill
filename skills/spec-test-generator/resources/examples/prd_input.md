# PRD: Internal User Directory API (MVP)

## Goal
Provide an internal API to list users for admin tools.

## Functional Requirements
1) Admin clients can list users with pagination.
2) User object includes id, email, and displayName.
3) Requests must be authenticated.
4) Error responses should be consistent and include a request ID.

## Non-Goals
- User creation, deletion, or password management.
- Public API support.

## Notes
- We want cursor pagination (not offset).
- p95 latency should be under 300ms for typical requests.

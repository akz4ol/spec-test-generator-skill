---
name: Spec & Test Generator
description: Converts PRDs/user stories into stable-ID requirements (REQ-xxxx), a structured test plan, a test case catalog (TEST-xxxx), and a traceability matrix. Supports iterative updates without renumbering IDs. Ships with pragmatic internal default and strict preset.
---

# Spec & Test Generator Skill

## Scope
Use this skill when you want to transform informal requirements (PRD, user stories, notes) into **auditable engineering artifacts**:
- `REQUIREMENTS.md` with stable IDs (`REQ-0001...`)
- `TEST_PLAN.md` aligned to a pragmatic test pyramid
- `TEST_CASES.md` with stable test IDs (`TEST-0001...`)
- `TRACEABILITY.csv` linking REQ <-> TEST

Default mode is **pragmatic internal**: sufficient rigor without heavy compliance overhead.
A strict preset is included for regulated/high-assurance workflows.

## Inputs expected
Provide one or more of:
- PRD markdown file (recommended): `prd.md`
- User story list / tickets export (markdown or text)
- Existing spec artifacts (optional), to preserve stable IDs

Optional:
- Target stack info: language/framework (pytest, jest, junit, etc.)
- Quality constraints (latency, security, privacy, reliability)

## Outputs produced (stable contract)
Write outputs to `spec/` (or a user-specified directory):

1) `REQUIREMENTS.md` (always)
- Requirements grouped by feature area
- Each requirement has: ID, statement, rationale, priority, acceptance criteria, edge cases, notes

2) `TEST_PLAN.md` (always)
- Unit/integration/e2e strategy
- Test data strategy
- Environment and CI assumptions
- Non-functional test considerations (security, performance) as applicable

3) `TEST_CASES.md` (always)
- Each test has: ID, title, type, priority, preconditions, steps, expected, requirements covered

4) `TRACEABILITY.csv` (always)
Columns: `REQ_ID,TEST_ID,TYPE,PRIORITY`

Optional:
- `tests/` skeletons in the selected framework (if requested)

## Stable ID rules (critical)
- Do not renumber existing REQ/TEST IDs when rerunning.
- If an item is edited, keep its ID unless the meaning changes substantially.
- If a requirement splits into two, keep original ID on the closest match and allocate a new ID for the new split requirement.
- Maintain an internal ID map file if present (recommended): `spec/.idmap.json`.

## Procedure
### Step 1 — Parse and segment input
- Identify feature areas / epics.
- Extract functional requirements and non-functional constraints.
- Record assumptions and clarifications needed (but do not block output).

### Step 2 — Generate requirements with stable IDs
For each feature area:
- Produce `REQ-xxxx` items with:
  - Statement (testable)
  - Priority (Must/Should/Could; or P0/P1/P2)
  - Rationale
  - Acceptance Criteria (Given/When/Then OR bullet checks)
  - Edge Cases (data bounds, concurrency, failure modes)
  - Notes (dependencies, open questions)

### Step 3 — Generate test plan
- Propose a pragmatic test pyramid:
  - Unit tests for pure logic and validators
  - Integration tests for service boundaries (DB, cache, external APIs)
  - E2E tests for top user flows (not everything)
- Include environment, data, and CI considerations.

### Step 4 — Generate test cases and traceability
For each requirement:
- Create at least one test mapped to it.
- Include negative tests for meaningful failure modes.
- If security/auth exists, include authz + abuse-path tests where applicable.

### Step 5 — Validate coverage
- Ensure every requirement has at least one test in `TRACEABILITY.csv`.
- Ensure test cases reference at least one requirement.
- If strict preset: enforce stronger criteria (see policy).

## Quality gates
- Every `REQ-xxxx` has at least one `TEST-xxxx`.
- Acceptance criteria are objectively verifiable (avoid subjective language).
- Edge cases include at least: invalid input, boundary values, and error handling.
- Keep artifacts concise enough to be useful, but complete enough to implement.

## Failure modes & recovery
- If input is ambiguous: list clarifications in an "Open Questions" section, but still produce best-effort requirements/tests.
- If scope is huge: produce an MVP slice first and explicitly mark what is deferred.

## Templates and examples
See:
- `resources/examples/` for demo PRD and expected artifacts.
- `resources/catalogs/` for edge-case libraries.
- `policy/` for default internal policy and strict preset.

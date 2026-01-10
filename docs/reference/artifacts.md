# Artifact Reference

## REQUIREMENTS.md

Contains all requirements organized by feature area.

### Structure

```markdown
# Requirements

## Assumptions
- List of assumptions

## Open Questions
- Unresolved questions from PRD

## Feature: Feature Name

### REQ-0001 (P0) — Short title
**Statement:** The system SHALL...
**Acceptance Criteria:**
- Given X, when Y, then Z

**Edge Cases:**
- Edge case 1
- Edge case 2
```

### Fields

| Field | Description |
|-------|-------------|
| ID | Stable identifier (REQ-xxxx) |
| Priority | P0, P1, or P2 |
| Statement | Testable requirement |
| Acceptance Criteria | Verification conditions |
| Edge Cases | Boundary/error scenarios |

## TEST_PLAN.md

Describes the overall test strategy.

### Structure

```markdown
# Test Plan

## Strategy
- **Unit tests**: Description
- **Integration tests**: Description
- **E2E tests**: Description

## Test Data
- Data requirements

## Environments
- **CI**: Unit + light integration
- **Staging**: Full test suite
```

## TEST_CASES.md

Contains all test cases.

### Structure

```markdown
# Test Cases

### TEST-0001 (Unit, P0) — Test title
**Requirements:** REQ-0001, REQ-0002
**Preconditions:** Setup requirements
**Steps:**
1. Step one
2. Step two
**Expected:**
- Expected result 1
- Expected result 2
```

## TRACEABILITY.csv

Links requirements to tests.

### Format

```csv
REQ_ID,TEST_ID,TYPE,PRIORITY
REQ-0001,TEST-0001,Unit,P0
REQ-0001,TEST-0002,Integration,P0
REQ-0002,TEST-0003,E2E,P1
```

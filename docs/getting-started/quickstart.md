# Quick Start

## Create a PRD

Create `prd.md`:

```markdown
# PRD: User Authentication

## Goal
Implement secure user authentication for the application.

## Functional Requirements
1) Users can register with email and password
2) Users can log in with credentials
3) Users can reset their password via email

## Non-Goals
- Social login (OAuth)
- Two-factor authentication

## Notes
- Passwords must be at least 8 characters
```

## Generate Artifacts

```bash
spec-test-generator prd.md
```

Output:
```
============================================================
Spec & Test Generation Complete
============================================================
PRD: prd.md

Summary:
  Requirements: 3
  Test Cases:   6
  Traceability: 6 mappings

Generated Artifacts:
  REQUIREMENTS.md: spec/REQUIREMENTS.md
  TEST_PLAN.md: spec/TEST_PLAN.md
  TEST_CASES.md: spec/TEST_CASES.md
  TRACEABILITY.csv: spec/TRACEABILITY.csv
```

## View Generated Requirements

```markdown
# Requirements

## Feature: User Authentication

### REQ-0001 (P0) — Users can register with email...
**Statement:** The system SHALL allow users to register with email and password.
**Acceptance Criteria:**
- Given valid email and password, when user submits registration, then account is created

**Edge Cases:**
- Invalid email format
- Password too short
```

## Python API

```python
from spec_test_generator import SpecTestGenerator

generator = SpecTestGenerator(prd_path="prd.md")

result = generator.generate()
print(f"Requirements: {len(result['requirements'])}")

artifacts = generator.write_artifacts()
```

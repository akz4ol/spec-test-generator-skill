# Spec & Test Generator

**Generate requirements and test artifacts from PRDs with stable IDs**

Spec & Test Generator transforms informal requirements (PRDs, user stories) into auditable engineering artifacts with stable, persistent IDs.

## Features

- **Stable IDs** - `REQ-xxxx` and `TEST-xxxx` IDs persist across iterations
- **Requirements Generation** - Structured requirements with acceptance criteria
- **Test Plan Generation** - Pragmatic test pyramid strategy
- **Test Case Generation** - Detailed test cases with preconditions and steps
- **Traceability Matrix** - Bidirectional REQ ↔ TEST mapping

## Quick Install

```bash
pip install spec-test-generator
```

## Quick Usage

```bash
# Generate artifacts from a PRD
spec-test-generator prd.md

# Use strict regulated policy
spec-test-generator prd.md --strict
```

## Output Artifacts

```
spec/
├── REQUIREMENTS.md   # REQ-0001, REQ-0002, ...
├── TEST_PLAN.md      # Unit/integration/e2e strategy
├── TEST_CASES.md     # TEST-0001, TEST-0002, ...
├── TRACEABILITY.csv  # REQ_ID <-> TEST_ID mapping
└── .idmap.json       # ID persistence
```

## Next Steps

- [Installation](getting-started/installation.md)
- [Quick Start Guide](getting-started/quickstart.md)
- [Stable ID System](guide/stable-ids.md)
- [Policy Configuration](guide/policies.md)

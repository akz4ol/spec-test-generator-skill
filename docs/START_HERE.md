# Start Here

Welcome to spec-test-generator! This guide will get you from zero to productive in 5 minutes.

## What Is This?

spec-test-generator converts PRDs and user stories into structured requirements, test plans, test cases, and traceability matrices — with stable IDs that survive regeneration.

**One-liner**: Turn a PRD into auditable, traceable specs without manually numbering everything.

## Mental Model

```
PRD Markdown → [Parser + ID Manager + Generator] → Requirements + Tests + Traceability
```

1. **Parser** extracts requirements from your PRD
2. **ID Manager** assigns stable IDs using content fingerprints
3. **Generator** creates test cases for each requirement
4. **Output** produces markdown specs + CSV traceability matrix

## 3-Minute Quickstart

### Install

```bash
pip install spec-test-generator
```

### Run Your First Generation

```bash
# Download a sample PRD
curl -O https://raw.githubusercontent.com/akz4ol/spec-test-generator-skill/main/skills/spec-test-generator/resources/examples/prd_input.md

# Generate specs
spec-test-generator prd_input.md
```

### See Stable IDs in Action

```bash
# Edit the PRD slightly
echo "- Additional note" >> prd_input.md

# Regenerate
spec-test-generator prd_input.md

# REQ-0001 is still REQ-0001!
```

## What You'll See

```
spec-test-generator v1.0.0

Processing: prd_input.md
Policy: default.internal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extracted:
  • Goals: 2
  • Functional Requirements: 8
  • Non-Functional Requirements: 3
  • Non-Goals: 2

Generated:
  • Requirements: 11 (REQ-0001 to REQ-0011)
  • Test Cases: 22 (TEST-0001 to TEST-0022)
  • Coverage: 100%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Artifacts written to: spec/
  • REQUIREMENTS.md
  • TEST_PLAN.md
  • TEST_CASES.md
  • TRACEABILITY.csv
  • .idmap.json (commit this!)
```

## Key Concepts

| Concept | What It Means |
|---------|---------------|
| **Stable ID** | REQ-0001 stays REQ-0001 even after edits (fingerprint-based) |
| **Fingerprint** | Hash of requirement content, used to track identity |
| **Traceability** | Bidirectional REQ ↔ TEST mapping |
| **Policy** | Configuration for strictness (internal vs. regulated) |
| **.idmap.json** | Persistence file for IDs — commit this to version control! |

## Common Workflows

### 1. Sprint Planning
```bash
# Convert epic to testable requirements
spec-test-generator epic.md --output ./sprint-42/
```

### 2. Compliance/Audit
```bash
# Use strict policy for full traceability
spec-test-generator prd.md --strict
# Submit TRACEABILITY.csv to auditors
```

### 3. Change Impact Analysis
```bash
# After PRD changes, regenerate and diff
spec-test-generator updated-prd.md
git diff spec/REQUIREMENTS.md
# See which requirements changed (IDs stay stable!)
```

## Your First PR Idea

Here are some ways to contribute:

1. **Add output format**: Support Gherkin/BDD output in `src/spec_test_generator/output.py`
2. **Improve parsing**: Handle more PRD formats in `src/spec_test_generator/parser.py`
3. **Add test templates**: Create reusable test case templates

See [CONTRIBUTING.md](../CONTRIBUTING.md) for setup instructions.

## Important: Commit .idmap.json!

The `.idmap.json` file is what makes IDs stable. **Always commit it!**

```bash
git add spec/.idmap.json
git commit -m "Track requirement/test ID mappings"
```

Without it, IDs will be reassigned on every machine.

## Next Steps

- [Architecture](ARCHITECTURE.md) — How the internals work
- [Policy Schema](reference/policy-schema.md) — All configuration options
- [FAQ](FAQ.md) — Common questions answered

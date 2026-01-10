# Frequently Asked Questions

## General

### What makes IDs "stable"?

IDs are based on content fingerprints (hashes), not sequential numbering. When you edit a requirement:
- Minor edits (typos, whitespace) → Same fingerprint → Same ID
- Major rewrites → Different fingerprint → New ID

This means REQ-0001 stays REQ-0001 even after regenerating the spec.

### Do I need to commit .idmap.json?

**Yes, always commit .idmap.json!**

This file stores the fingerprint-to-ID mappings. Without it:
- IDs will be reassigned on each machine
- Different team members get different IDs
- Historical references break

### What happens if I delete .idmap.json?

All IDs will be reallocated from scratch. REQ-0001 will likely refer to a different requirement than before. Bug reports, test runs, and discussions referencing old IDs will be invalid.

**Recovery**: Restore from git history.

### Is this an AI that writes my tests?

No. It structures and organizes tests, but you implement them. The tool generates:
- Test case titles and IDs
- Preconditions and step outlines
- Expected result templates

You fill in the actual test code.

---

## Installation & Setup

### How do I install this?

```bash
pip install spec-test-generator
```

Or from source:
```bash
git clone https://github.com/akz4ol/spec-test-generator-skill.git
cd spec-test-generator-skill
pip install -e .
```

### What Python versions are supported?

Python 3.10, 3.11, and 3.12.

### Can I use this in Docker?

Yes:
```bash
docker build -t spec-test-generator .
docker run --rm -v $(pwd):/prds spec-test-generator /prds/prd.md
```

---

## Usage

### What PRD format is expected?

Markdown with these sections (all optional but recommended):

```markdown
# PRD: Feature Name

## Goal
What this accomplishes

## Functional Requirements
1) First requirement
2) Second requirement

## Non-Functional Requirements
- Performance: p95 < 300ms

## Non-Goals
- Out of scope items
```

### How do I use strict mode?

```bash
spec-test-generator prd.md --strict
```

Strict mode requires:
- 2+ tests per requirement
- Negative test cases
- 4+ edge cases
- GWT format for acceptance criteria

### Where are the output files?

By default in `spec/`:
- `REQUIREMENTS.md` — Structured requirements with IDs
- `TEST_PLAN.md` — Test pyramid strategy
- `TEST_CASES.md` — Detailed test cases
- `TRACEABILITY.csv` — REQ ↔ TEST mapping
- `.idmap.json` — ID persistence (commit this!)

Custom directory:
```bash
spec-test-generator prd.md --output ./my-specs
```

### Can I regenerate without losing IDs?

Yes, that's the whole point! As long as `.idmap.json` exists, regeneration preserves IDs.

```bash
# First run
spec-test-generator prd.md
# Edit prd.md
# Second run - IDs preserved!
spec-test-generator prd.md
```

---

## Policies

### What's the difference between internal and strict policies?

| Aspect | Internal | Strict |
|--------|----------|--------|
| Min tests per requirement | 1 | 2 |
| Negative tests | Optional | Required |
| Edge cases | 2+ | 4+ |
| Acceptance criteria | GWT or bullets | GWT only |
| Traceability gaps | Allowed | Not allowed |

### How do I create a custom policy?

Create a YAML file:
```yaml
policy_name: my-company-standard
test_generation:
  min_tests_per_requirement: 3
  require_negative_tests: true
  min_edge_cases: 5
format:
  acceptance_criteria: gwt_only
```

Use it:
```bash
spec-test-generator prd.md --policy my-policy.yaml
```

---

## Traceability

### How do I find untested requirements?

Check `TRACEABILITY.csv`. Any REQ without a corresponding TEST is untested.

Or use the traceability report:
```bash
spec-test-generator prd.md --coverage-report
```

### Can I manually link tests to requirements?

Not currently. The tool generates links automatically. Manual overrides are on the roadmap.

### How do I handle test cases that cover multiple requirements?

Currently, each test case links to one requirement. For cross-cutting tests, either:
1. Create a synthetic requirement for the integration
2. Wait for multi-requirement linking (on roadmap)

---

## Troubleshooting

### "No requirements found"

The parser couldn't extract requirements. Check:
1. Is your PRD in markdown format?
2. Does it have recognizable sections (Goal, Requirements)?
3. Are requirements in bullet or numbered format?

Use `--verbose` to see parsing details.

### IDs changed unexpectedly

Check if `.idmap.json` was deleted or not committed. Without it, IDs are reallocated.

### "Fingerprint collision" warning

Two different requirements hashed to the same fingerprint. This is extremely rare. The tool allocates a new ID for the collision.

### Output files are empty

Check that your PRD has actual content. Empty sections produce empty outputs.

---

## Contributing

### How do I add a new output format?

1. Add formatter in `src/spec_test_generator/output.py`
2. Add CLI flag in `src/spec_test_generator/__main__.py`
3. Add documentation
4. Add tests

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### How do I improve PRD parsing?

The parser is in `src/spec_test_generator/parser.py`. Look for:
- Section header patterns
- Bullet extraction logic
- Fallback strategies

### How do I report a bug?

Open an issue at: https://github.com/akz4ol/spec-test-generator-skill/issues

Include:
- spec-test-generator version
- PRD input (or minimal reproduction)
- .idmap.json contents (if relevant)
- Expected vs. actual behavior

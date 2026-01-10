# Spec & Test Generator Skill

[![CI](https://github.com/akz4ol/spec-test-generator-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/akz4ol/spec-test-generator-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**A tool that generates requirements and tests from PRDs, using stable IDs that persist across iterations, enabling traceable and auditable specifications.**

---

## Why This Exists

- **Requirements decay into chaos** — Every PRD iteration means re-numbering, broken references, and "which REQ-0042 are we talking about?"
- **Test coverage is guesswork** — Without traceability, you can't prove which tests cover which requirements
- **Manual ID management is error-prone** — Engineers waste time maintaining spreadsheets of REQ/TEST mappings
- **Regeneration breaks everything** — Edit a PRD and all your test case IDs shift, invalidating bug reports and test runs

## What It Is

- A **PRD parser** that extracts functional and non-functional requirements
- A **stable ID generator** using content fingerprints (IDs survive edits)
- A **test case generator** with pragmatic test pyramid strategy
- A **traceability matrix builder** for REQ ↔ TEST bidirectional mapping
- **Audit-ready** — generates artifacts suitable for compliance and reviews

## What It Is NOT

- Not an AI that writes your tests (it structures them, you implement them)
- Not a test runner or execution framework
- Not a requirements management system (it generates snapshots, not a database)
- Not a replacement for thinking — garbage PRD in, garbage specs out

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Spec & Test Generation Pipeline                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────────┐   │
│  │   PRD    │───▶│  Parser  │───▶│     Extracted Requirements   │   │
│  │ Markdown │    │          │    │  (goals, FRs, NFRs, scope)   │   │
│  └──────────┘    └──────────┘    └──────────────────────────────┘   │
│                                         │                            │
│                        ┌────────────────┘                            │
│                        ▼                                             │
│  ┌──────────┐    ┌────────────┐    ┌────────────────────────────┐   │
│  │ .idmap   │◀──▶│ ID Manager │───▶│   Stable IDs (REQ-xxxx)    │   │
│  │  .json   │    │ (fingerprint)   │   Persist across edits     │   │
│  └──────────┘    └────────────┘    └────────────────────────────┘   │
│                                         │                            │
│                        ┌────────────────┘                            │
│                        ▼                                             │
│               ┌──────────────┐    ┌────────────────────────────┐    │
│               │  Generator   │───▶│   Test Cases (TEST-xxxx)   │    │
│               │              │    │   with preconditions/steps │    │
│               └──────────────┘    └────────────────────────────┘    │
│                                         │                            │
│                        ┌────────────────┘                            │
│                        ▼                                             │
│               ┌─────────────────────────────────────────────────┐   │
│               │              Output Artifacts                    │   │
│               │  • REQUIREMENTS.md  (structured requirements)   │   │
│               │  • TEST_PLAN.md     (test pyramid strategy)     │   │
│               │  • TEST_CASES.md    (detailed test cases)       │   │
│               │  • TRACEABILITY.csv (REQ ↔ TEST mapping)        │   │
│               └─────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 30-Second Hello World

```bash
pip install spec-test-generator

# Generate specs from a PRD
spec-test-generator prd.md
```

### 2-Minute Realistic Example

```bash
# Generate with strict policy (regulated environments)
spec-test-generator prd.md --strict --output ./specs

# Output files created:
# specs/REQUIREMENTS.md   - 12 requirements (REQ-0001 to REQ-0012)
# specs/TEST_PLAN.md      - Test strategy with pyramid breakdown
# specs/TEST_CASES.md     - 24 test cases (TEST-0001 to TEST-0024)
# specs/TRACEABILITY.csv  - Full coverage matrix
# specs/.idmap.json       - ID persistence (commit this!)

# Edit prd.md, regenerate - IDs stay stable!
spec-test-generator prd.md --strict --output ./specs
# REQ-0001 still refers to the same requirement
```

### Python API

```python
from spec_test_generator import SpecTestGenerator

generator = SpecTestGenerator(prd_path="prd.md")

result = generator.generate()
print(f"Requirements: {len(result['requirements'])}")
print(f"Test Cases: {len(result['test_cases'])}")

# Write artifacts to disk
artifacts = generator.write_artifacts(output_dir="./specs")
```

### Docker

```bash
docker build -t spec-test-generator .
docker run --rm -v $(pwd):/prds spec-test-generator /prds/prd.md
```

---

## Real-World Use Cases

| Use Case | Command | Outcome |
|----------|---------|---------|
| **Sprint planning** | `spec-test-generator epic.md` | Break epics into testable requirements |
| **Compliance audit** | `spec-test-generator prd.md --strict` | Generate audit-ready traceability |
| **Test coverage analysis** | Check `TRACEABILITY.csv` | Identify untested requirements |
| **Change impact** | Regenerate after PRD edit | See which tests need updating |

---

## Comparison with Alternatives

| Tool | Focus | Stable IDs | Traceability | Regeneration |
|------|-------|------------|--------------|--------------|
| **spec-test-generator** | PRD → Specs + Tests | Yes (fingerprint) | Full matrix | Safe |
| Jira/Linear | Issue tracking | Manual | Manual links | N/A |
| TestRail | Test management | Sequential | Manual | Breaks refs |
| AI assistants | Ad-hoc generation | No | No | Full rewrite |

**Key differentiator**: Fingerprint-based IDs that survive edits — your bug reports and test runs reference stable identifiers.

---

## Stable ID System

IDs use content fingerprints to survive regeneration:

| Edit Type | ID Behavior |
|-----------|-------------|
| Minor wording change | Same ID retained |
| Requirement split | Original ID on closest match |
| Major rewrite | New ID allocated |
| Requirement deleted | ID retired (never reused) |

### How It Works

```json
// .idmap.json (commit this file!)
{
  "requirements": {
    "a1b2c3d4": "REQ-0001",  // fingerprint → stable ID
    "e5f6g7h8": "REQ-0002"
  },
  "tests": {
    "x9y0z1a2": "TEST-0001"
  },
  "next_req_id": 3,
  "next_test_id": 2
}
```

---

## Policies

| Policy | Use Case | Min Tests/Req | Negative Tests |
|--------|----------|---------------|----------------|
| `default.internal.yaml` | Internal/agile | 1 | Optional |
| `preset.strict.yaml` | Regulated/compliance | 2 | Required |

### Policy Differences

| Feature | Internal | Strict |
|---------|----------|--------|
| Minimum tests per requirement | 1 | 2 |
| Negative test cases | Optional | Required |
| Edge cases per requirement | 2+ | 4+ |
| Acceptance criteria format | GWT or bullets | GWT only |
| Traceability completeness | Optional gaps | 100% coverage |

---

## PRD Input Format

```markdown
# PRD: Feature Name

## Goal
What this feature accomplishes (1-2 sentences)

## Functional Requirements
1) User can do X when Y
2) System shall Z under condition W

## Non-Functional Requirements
- Performance: p95 < 300ms
- Security: All endpoints require authentication

## Non-Goals
- Things explicitly out of scope
- Features we're not building

## Notes
- Additional context for implementers
```

---

## Output Artifacts

```
specs/
├── REQUIREMENTS.md   # REQ-0001, REQ-0002, ... with acceptance criteria
├── TEST_PLAN.md      # Test pyramid strategy (unit/integration/e2e)
├── TEST_CASES.md     # TEST-0001, TEST-0002, ... with steps
├── TRACEABILITY.csv  # REQ_ID,TEST_ID,Coverage mapping
└── .idmap.json       # ID persistence store (commit this!)
```

---

## Additional Features

### Gherkin/BDD Output
Generate `.feature` files from requirements:

```python
from spec_test_generator import GherkinGenerator

generator = GherkinGenerator(result, output_dir)
artifacts = generator.generate()
# Creates features/authentication.feature, features/payment.feature, etc.
```

### Import from Jira/Linear
Import requirements from existing issue trackers:

```python
from spec_test_generator import JiraImporter, LinearImporter, IDManager

id_manager = IDManager(output_dir)

# From Jira JSON export
jira = JiraImporter(id_manager)
requirements = jira.import_from_file("jira_export.json")

# From Linear JSON export
linear = LinearImporter(id_manager)
requirements = linear.import_from_file("linear_export.json")
```

### Test Coverage Gap Analysis
Identify requirements without adequate test coverage:

```python
from spec_test_generator import CoverageAnalyzer

analyzer = CoverageAnalyzer(result)
report = analyzer.analyze()

print(f"Coverage: {report.coverage_percentage}%")
for gap in report.gaps:
    print(f"  {gap.req_id}: {gap.gap_type} - {gap.description}")

# Write report
analyzer.write_report(output_dir)  # Creates COVERAGE_REPORT.md
```

### Change Impact Reports
Compare PRD versions and analyze impact:

```python
from spec_test_generator import ImpactAnalyzer

analyzer = ImpactAnalyzer(output_dir)
report = analyzer.compare("prd_v1.md", "prd_v2.md", existing_tests)

print(f"Risk Level: {report.risk_level}")
print(f"Changes: {len(report.changes)}")
print(f"Affected Tests: {report.affected_tests}")

# Write report
analyzer.write_report("prd_v1.md", "prd_v2.md")  # Creates IMPACT_REPORT.md
```

---

## Roadmap

### Now ✅
- [x] PRD markdown parsing
- [x] Stable ID generation with fingerprinting
- [x] Requirements, test plan, test case generation
- [x] CSV traceability matrix
- [x] Gherkin/BDD output format
- [x] Import from Jira/Linear
- [x] Test coverage gap analysis
- [x] Change impact reports

### Next
- [ ] IDE plugins (VS Code, IntelliJ)
- [ ] Integration with TestRail/Zephyr
- [ ] AI-assisted test case expansion

### Later
- [ ] Real-time PRD collaboration
- [ ] Multi-language support

---

## Development

```bash
git clone https://github.com/akz4ol/spec-test-generator-skill.git
cd spec-test-generator-skill
pip install -e ".[dev]"

make test    # Run tests
make lint    # Run linters
make format  # Format code
make all     # All checks
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Good first issues:**
- Add new output format (Gherkin, XML)
- Improve PRD parsing edge cases
- Add test case templates

---

## Documentation

- [Getting Started](docs/START_HERE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/reference/python-api.md)
- [Policy Schema](docs/reference/policy-schema.md)
- [FAQ](docs/FAQ.md)
- [Architectural Decisions](docs/DECISIONS.md)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

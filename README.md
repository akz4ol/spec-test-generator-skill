# Spec & Test Generator Skill

[![CI](https://github.com/yourorg/spec-test-generator-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/yourorg/spec-test-generator-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Converts PRDs and user stories into stable-ID requirements, test plans, test cases, and traceability matrices.

## Features

- **Stable IDs**: `REQ-xxxx` and `TEST-xxxx` IDs persist across iterations
- **Requirements Generation**: Structured requirements with acceptance criteria
- **Test Plan Generation**: Pragmatic test pyramid strategy
- **Test Case Generation**: Detailed test cases with preconditions and steps
- **Traceability Matrix**: Bidirectional REQ ↔ TEST mapping
- **Policy-Driven**: Configurable strictness levels

## Installation

```bash
# From PyPI
pip install spec-test-generator

# From source
git clone https://github.com/yourorg/spec-test-generator-skill.git
cd spec-test-generator-skill
pip install -e ".[dev]"
```

## Quick Start

### CLI Usage

```bash
# Generate spec artifacts from PRD
spec-test-generator prd.md

# Use strict regulated policy
spec-test-generator prd.md --strict

# Output as JSON
spec-test-generator prd.md --json

# Custom output directory
spec-test-generator prd.md --output ./spec-docs
```

### Python API

```python
from spec_test_generator import SpecTestGenerator

generator = SpecTestGenerator(prd_path="prd.md")

result = generator.generate()
print(f"Requirements: {len(result['requirements'])}")
print(f"Test Cases: {len(result['test_cases'])}")

# Write artifacts
artifacts = generator.write_artifacts()
```

### Docker

```bash
# Build image
docker build -t spec-test-generator .

# Generate from PRD
docker run --rm -v $(pwd):/prds spec-test-generator /prds/prd.md
```

## Output Artifacts

```
spec/
├── REQUIREMENTS.md   # REQ-0001, REQ-0002, ...
├── TEST_PLAN.md      # Unit/integration/e2e strategy
├── TEST_CASES.md     # TEST-0001, TEST-0002, ...
├── TRACEABILITY.csv  # REQ_ID <-> TEST_ID mapping
└── .idmap.json       # ID persistence (internal)
```

## Policies

| Policy | Use Case |
|--------|----------|
| `default.internal.yaml` | Pragmatic internal workflows (default) |
| `preset.strict.yaml` | Regulated/high-assurance environments |

### Policy Differences

| Feature | Internal | Strict |
|---------|----------|--------|
| Min tests per req | 1 | 2 |
| Negative tests | Optional | Required |
| Edge cases | 2+ | 4+ |
| Acceptance criteria | GWT or bullets | GWT only |

## PRD Input Format

```markdown
# PRD: Feature Name

## Goal
What this feature accomplishes

## Functional Requirements
1) First requirement
2) Second requirement

## Non-Functional Requirements
- Performance: p95 < 300ms

## Non-Goals
- Things explicitly out of scope

## Notes
- Additional context
```

## Stable ID System

IDs are fingerprint-based and persist across regenerations:

- **Minor edits** → Same ID retained
- **Requirement split** → Original ID on closest match
- **Major rewrite** → New ID allocated

The `.idmap.json` file stores mappings:

```json
{
  "requirements": {
    "fingerprint123": "REQ-0001"
  },
  "tests": {
    "testhash789": "TEST-0001"
  }
}
```

## Directory Structure

```
spec-test-generator-skill/
├── src/spec_test_generator/  # Python package
├── skills/spec-test-generator/  # Skill definition
│   ├── SKILL.md              # Skill documentation
│   ├── policy/               # Policy presets
│   └── resources/            # Examples
├── tests/                    # Test suite
├── schemas/                  # JSON schemas
├── docs/                     # Documentation
├── Dockerfile                # Container support
└── Makefile                 # Common tasks
```

## Development

```bash
# Install dev dependencies
make dev

# Run tests
make test

# Run linters
make lint

# Format code
make format

# Run all checks
make all
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Documentation

- [API Documentation](docs/API.md)
- [Skill Definition](skills/spec-test-generator/SKILL.md)
- [Changelog](CHANGELOG.md)

# Spec & Test Generator - API Documentation

## Python API

### Quick Start

```python
from spec_test_generator import SpecTestGenerator

# Basic usage
generator = SpecTestGenerator(
    prd_path="prd.md",
)

# Generate artifacts
result = generator.generate()
print(f"Requirements: {len(result['requirements'])}")
print(f"Test Cases: {len(result['test_cases'])}")

# Write to files
artifacts = generator.write_artifacts()
for name, path in artifacts.items():
    print(f"Generated: {path}")
```

### SpecTestGenerator Class

```python
class SpecTestGenerator:
    def __init__(
        self,
        prd_path: str | Path,
        policy_path: str | Path | None = None,
        output_dir: str | Path = "spec",
    ):
        """
        Initialize generator.

        Args:
            prd_path: Path to PRD markdown file
            policy_path: Path to policy YAML (default: pragmatic internal)
            output_dir: Directory for output artifacts
        """

    def generate(self) -> dict[str, Any]:
        """
        Generate all spec and test artifacts.

        Returns:
            Dict with requirements, test_plan, test_cases, traceability
        """

    def write_artifacts(self, result: dict | None = None) -> dict[str, Path]:
        """
        Write artifacts to output directory.

        Args:
            result: Previous generation result (runs generate() if not provided)

        Returns:
            Dict mapping artifact names to file paths
        """
```

### Requirement

```python
@dataclass
class Requirement:
    id: str                          # e.g., "REQ-0001"
    statement: str                   # The requirement statement
    priority: Priority               # P0, P1, P2
    acceptance_criteria: list[str]   # Given-When-Then or bullets
    edge_cases: list[str]            # Edge case scenarios
    rationale: str | None            # Why this requirement exists
    notes: str | None                # Additional notes
    feature_area: str | None         # Feature grouping
```

### TestCase

```python
@dataclass
class TestCase:
    id: str                          # e.g., "TEST-0001"
    title: str                       # Test title
    test_type: TestType              # Unit, Integration, E2E
    priority: Priority               # P0, P1, P2
    requirement_ids: list[str]       # Linked requirements
    preconditions: str | None        # Setup requirements
    steps: list[str]                 # Test steps
    expected: list[str]              # Expected results
```

### TestPlan

```python
@dataclass
class TestPlan:
    strategy: dict[str, str]         # Test type -> description
    test_data: list[str]             # Test data considerations
    environments: dict[str, str]     # Environment -> description
    non_functional: list[str]        # Non-functional test notes
```

### TraceabilityEntry

```python
@dataclass
class TraceabilityEntry:
    req_id: str                      # Requirement ID
    test_id: str                     # Test case ID
    test_type: TestType              # Test type
    priority: Priority               # Priority level
```

## CLI Reference

```bash
# Basic usage
spec-test-generator prd.md

# Use strict regulated policy
spec-test-generator prd.md --strict

# Custom policy
spec-test-generator prd.md --policy my-policy.yaml

# Output as JSON
spec-test-generator prd.md --json

# Custom output directory
spec-test-generator prd.md --output ./spec-docs
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | File not found |
| 3 | Other error |

## Stable ID System

### How IDs Work

- IDs are generated based on content fingerprints
- Running the generator multiple times preserves IDs
- The `.idmap.json` file stores ID mappings

### ID Preservation Rules

1. **Minor edits**: Same ID retained
2. **Requirement split**: Original ID kept on closest match, new ID for split
3. **Major rewrite**: New ID allocated

### ID Map Format

```json
{
  "requirements": {
    "fingerprint123": "REQ-0001",
    "fingerprint456": "REQ-0002"
  },
  "tests": {
    "testhash789": "TEST-0001"
  },
  "metadata": {
    "version": "1.0",
    "req_prefix": "REQ",
    "test_prefix": "TEST"
  }
}
```

## Policy Configuration

See `policy/default.internal.yaml` for the full policy structure.

### Key Policy Sections

```yaml
ids:
  requirement_prefix: "REQ"
  test_prefix: "TEST"
  pad: 4  # Zero-padding width

requirements:
  fields_required:
    - statement
    - priority
    - acceptance_criteria
  min_edge_cases_per_requirement: 2

tests:
  require_min_tests_per_requirement: 1
  include_negative_tests: true
  e2e_selection_rule: "only_top_flows"

traceability:
  required: true
  fail_if_requirement_missing_tests: true
```

## PRD Input Format

The generator expects markdown with these sections:

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

### Supported Section Headers

- Goal / Objective
- Functional Requirements / Requirements
- Non-Functional Requirements / NFR
- Non-Goals / Out of Scope
- Notes
- Assumptions

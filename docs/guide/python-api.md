# Python API

## SpecTestGenerator Class

```python
from spec_test_generator import SpecTestGenerator

generator = SpecTestGenerator(
    prd_path="prd.md",
    policy_path="policy.yaml",  # optional
    output_dir="spec",          # optional
)
```

### Methods

#### `generate() -> dict`

Generate all artifacts.

```python
result = generator.generate()
print(result['requirements'])  # List of Requirement objects
print(result['test_cases'])    # List of TestCase objects
print(result['traceability'])  # List of TraceabilityEntry objects
```

#### `write_artifacts(result=None) -> dict[str, Path]`

Write artifacts to files.

```python
artifacts = generator.write_artifacts()
# {'REQUIREMENTS.md': Path('spec/REQUIREMENTS.md'), ...}
```

## Data Models

### Requirement

```python
@dataclass
class Requirement:
    id: str                          # e.g., "REQ-0001"
    statement: str
    priority: Priority               # P0, P1, P2
    acceptance_criteria: list[str]
    edge_cases: list[str]
    rationale: str | None
    notes: str | None
    feature_area: str | None
```

### TestCase

```python
@dataclass
class TestCase:
    id: str                          # e.g., "TEST-0001"
    title: str
    test_type: TestType              # Unit, Integration, E2E
    priority: Priority
    requirement_ids: list[str]       # Linked requirements
    preconditions: str | None
    steps: list[str]
    expected: list[str]
```

### TraceabilityEntry

```python
@dataclass
class TraceabilityEntry:
    req_id: str
    test_id: str
    test_type: TestType
    priority: Priority
```

# Architecture

This document describes the internal architecture of spec-test-generator.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        spec-test-generator                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────────────┐ │
│  │   CLI Layer    │───▶│   Generator    │───▶│   Output Generator    │ │
│  │  (__main__.py) │    │ (generator.py) │    │    (output.py)        │ │
│  └────────────────┘    └───────┬────────┘    └────────────────────────┘ │
│                                │                                         │
│                    ┌───────────┼───────────┐                            │
│                    ▼           ▼           ▼                            │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │     Parser     │  │  ID Manager    │  │   Test Case    │            │
│  │  (parser.py)   │  │ (id_manager.py)│  │   Generator    │            │
│  └────────────────┘  └────────────────┘  └────────────────┘            │
│                                │                                         │
│                                ▼                                         │
│                     ┌────────────────────┐                              │
│                     │   .idmap.json      │                              │
│                     │   (persistence)    │                              │
│                     └────────────────────┘                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Problem Statement

Converting PRDs to specs and tests is manual and error-prone:
- Sequential IDs break when requirements change
- No traceability between requirements and tests
- Regeneration invalidates bug reports and test runs
- Different team members create inconsistent formats

## Non-Goals

- **Test implementation**: We structure tests, you implement them
- **Test execution**: We're not a test runner
- **Requirements database**: We generate snapshots, not a live system
- **AI writing**: We structure and organize, not hallucinate content

## Invariants

1. **Fingerprint stability**: Same content → same fingerprint → same ID
2. **ID uniqueness**: Each ID is allocated exactly once, never reused
3. **Traceability completeness**: Every requirement has at least one test
4. **Output determinism**: Same input + same .idmap.json → same output

## Data Model

### Core Types

```python
@dataclass
class Requirement:
    id: str              # e.g., "REQ-0001"
    fingerprint: str     # Content hash for stability
    title: str           # Short description
    description: str     # Full requirement text
    type: str            # FUNCTIONAL, NON_FUNCTIONAL
    priority: Priority   # HIGH, MEDIUM, LOW
    acceptance_criteria: list[str]

@dataclass
class TestCase:
    id: str              # e.g., "TEST-0001"
    fingerprint: str     # Content hash for stability
    title: str           # Test case name
    requirement_id: str  # Links to REQ-xxxx
    type: TestType       # UNIT, INTEGRATION, E2E
    preconditions: list[str]
    steps: list[str]
    expected_result: str

@dataclass
class TraceabilityEntry:
    req_id: str
    test_id: str
    req_summary: str
    test_summary: str
```

### ID Map Structure

```json
{
  "requirements": {
    "a1b2c3d4e5f6": "REQ-0001",
    "b2c3d4e5f6g7": "REQ-0002"
  },
  "tests": {
    "x1y2z3a4b5c6": "TEST-0001"
  },
  "next_req_id": 3,
  "next_test_id": 2,
  "retired_ids": ["REQ-0005"]
}
```

## Key Algorithms

### 1. Fingerprint Generation

```python
def fingerprint(text: str) -> str:
    normalized = text.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    return hashlib.sha256(normalized.encode()).hexdigest()[:12]
```

Key properties:
- Whitespace-insensitive
- Case-insensitive
- Deterministic

### 2. ID Allocation

```python
def allocate_id(fingerprint: str, namespace: str) -> str:
    if fingerprint in idmap[namespace]:
        return idmap[namespace][fingerprint]  # Existing ID

    new_id = f"{PREFIX}-{next_id:04d}"
    idmap[namespace][fingerprint] = new_id
    next_id += 1
    return new_id
```

Key properties:
- Idempotent: same fingerprint always gets same ID
- Monotonic: IDs always increase
- Persistent: allocations survive across runs via .idmap.json

### 3. PRD Parsing

```python
def parse_prd(content: str) -> ParsedPRD:
    sections = split_by_headers(content)

    return ParsedPRD(
        goals=extract_goals(sections.get("goal", "")),
        functional_reqs=extract_bullets(sections.get("functional requirements", "")),
        non_functional_reqs=extract_bullets(sections.get("non-functional requirements", "")),
        non_goals=extract_bullets(sections.get("non-goals", "")),
    )
```

Best-effort parsing with fallbacks for missing sections.

### 4. Test Case Generation

```python
def generate_tests(requirement: Requirement, policy: Policy) -> list[TestCase]:
    tests = []

    # Happy path
    tests.append(create_positive_test(requirement))

    # Negative cases (if policy requires)
    if policy.require_negative_tests:
        tests.extend(create_negative_tests(requirement))

    # Edge cases
    tests.extend(create_edge_case_tests(requirement, policy.min_edge_cases))

    return tests
```

Policy controls test quantity and types.

## Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `__main__.py` | CLI argument parsing, orchestration |
| `generator.py` | Main coordination, runs pipeline |
| `parser.py` | PRD markdown parsing, section extraction |
| `id_manager.py` | Fingerprinting, ID allocation, persistence |
| `models.py` | Data classes for requirements, tests |
| `output.py` | Markdown/CSV artifact generation |

## Extension Points

### Adding a New Output Format

1. Add formatter to `output.py`:
```python
def format_gherkin(test_case: TestCase) -> str:
    return f"""
Feature: {test_case.title}
  Scenario: {test_case.title}
    Given {test_case.preconditions[0]}
    When {test_case.steps[0]}
    Then {test_case.expected_result}
"""
```

2. Add CLI flag in `__main__.py`:
```python
parser.add_argument('--format', choices=['markdown', 'gherkin'])
```

### Adding a New Test Type

1. Add to `TestType` enum in `models.py`
2. Add generation logic in `generator.py`
3. Update templates in `output.py`

## Threat Model (Lightweight)

| Threat | Mitigation |
|--------|------------|
| Malicious PRD crashes parser | Exception handling, graceful degradation |
| .idmap.json tampering | JSON validation on load |
| ID collision | SHA-256 fingerprints (collision-resistant) |
| Large PRD DoS | Reasonable size limits |

## Performance Assumptions

- **PRD size**: < 1MB, < 200 requirements
- **Processing time**: < 2 seconds for typical PRD
- **Memory**: < 200MB peak
- **.idmap.json size**: < 1MB (10K+ requirements)

For larger specs, consider splitting into multiple PRDs.

## Trade-offs and Failure Modes

### Trade-off: Fingerprint Sensitivity

Too sensitive: minor edits create new IDs
Too lenient: different requirements get same ID

**Current approach**: Normalize whitespace and case, hash first 12 chars of SHA-256.

**Result**: Typo fixes preserve ID, substantial rewrites get new ID.

### Trade-off: .idmap.json Dependency

IDs only stable if .idmap.json is preserved.

**Mitigation**: Clear documentation to commit .idmap.json. Warn if file missing.

### Trade-off: Test Quality vs. Quantity

Generating many tests is easy. Generating good tests is hard.

**Approach**: Generate structure (preconditions, steps), human fills implementation details.

### Failure Mode: Ambiguous PRD Structure

PRDs without standard headers may parse incorrectly.

**Mitigation**: Document expected format, fallback to bullet extraction, emit warnings.

### Failure Mode: Merge Conflicts in .idmap.json

Two branches adding requirements simultaneously will conflict.

**Current**: Standard JSON merge (manual resolution)
**Future**: Consider CRDT-style merge strategy

### Failure Mode: Fingerprint Collision

Theoretically possible but astronomically unlikely with SHA-256.

**Mitigation**: If detected, warn and allocate new ID.

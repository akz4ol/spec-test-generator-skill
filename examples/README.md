# Spec & Test Generator Examples

This directory contains working examples demonstrating the Spec & Test Generator.

## Quick Start

```bash
# From the repository root
cd examples
python run_example.py
```

## Files

- `sample_prd.md` - Example PRD (Product Requirements Document)
- `run_example.py` - Script demonstrating all features
- `output/` - Generated artifacts (created after running)

## Generated Artifacts

After running the example, you'll find:

```
output/
├── REQUIREMENTS.md      # Formal requirements with stable IDs
├── TEST_PLAN.md         # Test strategy and approach
├── TEST_CASES.md        # Individual test cases
├── TRACEABILITY.csv     # Requirement-to-test mapping
├── COVERAGE_REPORT.md   # Test coverage analysis
├── .idmap.json          # ID persistence (commit this!)
└── features/            # Gherkin feature files
    └── user_authentication_system.feature
```

## Sample Output

### Requirements
```markdown
### REQ-0001 (P0) — The system SHALL allow...
**Statement:** The system SHALL allow users to register with email and password
**Acceptance Criteria:**
- Given valid input, when the operation is performed, then allow users to register
- Given invalid input, when the operation is attempted, then return appropriate error

**Edge Cases:**
- Invalid input format
- Boundary value conditions
```

### Gherkin Feature
```gherkin
Feature: User Authentication System
  As a user
  I want user authentication system functionality
  So that the system meets requirements

  @REQ-0001 @P0
  Scenario: Verify user registration
    Given Valid test environment setup
    When set up test preconditions
    And execute the operation
    Then operation succeeds
```

## Customization

You can customize generation by providing a policy file:

```python
generator = SpecTestGenerator(
    prd_path="my_prd.md",
    policy_path="my_policy.yaml",  # Custom policy
    output_dir="spec",
)
```

See `skills/spec-test-generator/policy/default.internal.yaml` for policy options.

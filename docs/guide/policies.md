# Policies

## Built-in Policies

### Pragmatic Internal (Default)

For internal workflows with reasonable rigor:

```bash
spec-test-generator prd.md
```

Key settings:
- 1+ test per requirement
- 2+ edge cases per requirement
- Negative tests optional
- GWT or bullet acceptance criteria

### Strict Regulated

For regulated/high-assurance environments:

```bash
spec-test-generator prd.md --strict
```

Key settings:
- 2+ tests per requirement
- 4+ edge cases per requirement
- 1+ negative test per requirement
- Given-When-Then format required
- Bidirectional traceability notes

## Policy Comparison

| Feature | Internal | Strict |
|---------|----------|--------|
| Min tests per req | 1 | 2 |
| Min negative tests | 0 | 1 |
| Min edge cases | 2 | 4 |
| Acceptance format | GWT or bullets | GWT only |
| Traceability notes | Optional | Required |

## Custom Policies

Create a YAML file:

```yaml
policy_name: "My Custom Policy"
policy_version: "1.0"

ids:
  requirement_prefix: "REQ"
  test_prefix: "TEST"
  pad: 4

requirements:
  fields_required:
    - statement
    - priority
    - acceptance_criteria
    - edge_cases
  min_edge_cases_per_requirement: 3

tests:
  require_min_tests_per_requirement: 2
  include_negative_tests: true
  min_negative_tests_per_requirement: 1

traceability:
  required: true
  fail_if_requirement_missing_tests: true
```

Use it:

```bash
spec-test-generator prd.md --policy my-policy.yaml
```

# Policy Schema Reference

## Top-Level Fields

```yaml
policy_name: string      # Required
policy_version: string   # Required
```

## IDs

```yaml
ids:
  requirement_prefix: string  # Default: "REQ"
  test_prefix: string         # Default: "TEST"
  pad: integer                # Default: 4 (zero-padding)
  preserve_existing_ids: boolean
```

## Requirements

```yaml
requirements:
  fields_required:
    - statement
    - priority
    - rationale          # Optional
    - acceptance_criteria
    - edge_cases
    - out_of_scope       # Optional
  priority_scale:
    - P0
    - P1
    - P2
  acceptance_criteria_style: given-when-then | bullets | given-when-then_or_bullets
  min_edge_cases_per_requirement: integer
  include_open_questions_section: boolean
```

## Tests

```yaml
tests:
  require_min_tests_per_requirement: integer
  include_negative_tests: boolean
  min_negative_tests_per_requirement: integer
  include_security_tests_if_auth_present: boolean
  require_security_tests_for_sensitive_data: boolean
  types:
    unit: boolean
    integration: boolean
    e2e: boolean
  e2e_selection_rule: only_top_flows | all_p0_flows | all_flows
```

## Traceability

```yaml
traceability:
  required: boolean
  fail_if_requirement_missing_tests: boolean
  fail_if_test_missing_requirements: boolean
  require_bidirectional_traceability_notes: boolean
```

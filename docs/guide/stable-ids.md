# Stable ID System

## Overview

The Spec & Test Generator uses a fingerprint-based ID system that ensures IDs remain stable across regenerations.

## How It Works

1. **Fingerprinting**: Each requirement/test gets a fingerprint based on its content
2. **ID Mapping**: Fingerprints are mapped to stable IDs (REQ-0001, TEST-0001)
3. **Persistence**: Mappings are stored in `.idmap.json`

## ID Persistence Rules

| Scenario | Behavior |
|----------|----------|
| Minor text edit | Same ID retained |
| Requirement split | Original ID on closest match |
| Major rewrite | New ID allocated |
| Requirement removed | ID not reused |

## Example

First run:
```
REQ-0001: Users can log in
REQ-0002: Users can log out
```

Second run (after minor edit):
```
REQ-0001: Users can log in with credentials  # Same ID!
REQ-0002: Users can log out
REQ-0003: Users can reset password  # New requirement
```

## ID Map File

The `.idmap.json` file stores the mappings:

```json
{
  "requirements": {
    "abc123def456": "REQ-0001",
    "789ghi012jkl": "REQ-0002"
  },
  "tests": {
    "mno345pqr678": "TEST-0001"
  },
  "metadata": {
    "version": "1.0",
    "req_prefix": "REQ",
    "test_prefix": "TEST"
  }
}
```

## Custom Prefixes

Configure in your policy:

```yaml
ids:
  requirement_prefix: "SPEC"
  test_prefix: "TC"
  pad: 4
```

Result: `SPEC-0001`, `TC-0001`

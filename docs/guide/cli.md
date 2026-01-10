# CLI Reference

## Synopsis

```bash
spec-test-generator [OPTIONS] PRD
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PRD` | Path to PRD markdown file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--policy PATH` | Path to policy YAML file |
| `-o, --output PATH` | Output directory (default: `spec/`) |
| `--json` | Output as JSON instead of artifacts |
| `--strict` | Use strict regulated policy |

## Examples

### Basic Generation
```bash
spec-test-generator prd.md
```

### Strict Policy
```bash
spec-test-generator prd.md --strict
```

### JSON Output
```bash
spec-test-generator prd.md --json | jq '.requirements'
```

### Custom Output Directory
```bash
spec-test-generator prd.md -o ./requirements
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | File not found |
| 3 | Other error |

# Benchmarks

This directory contains performance benchmarks for spec-test-generator.

## Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| Parse time | Time to parse PRD markdown | < 100ms for 100 requirements |
| ID allocation | Time to allocate/lookup IDs | < 50ms for 100 requirements |
| Generation time | Time to generate all artifacts | < 500ms for 100 requirements |
| Memory peak | Maximum memory during processing | < 200MB |

## Running Benchmarks

```bash
# Run all benchmarks
./benchmark.sh

# Run specific benchmark
python benchmark_id_manager.py
```

## Test PRDs

| PRD | Requirements | Size |
|-----|--------------|------|
| `prds/small.md` | 10 | ~2KB |
| `prds/medium.md` | 50 | ~10KB |
| `prds/large.md` | 200 | ~40KB |

## Results

See [results.md](results.md) for latest benchmark results.

## ID Manager Performance

The ID manager is critical for performance:

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Fingerprint | O(n) | n = content length |
| ID lookup | O(1) | Hash table lookup |
| ID allocation | O(1) | Increment counter |
| Save .idmap.json | O(m) | m = total mappings |

## Contributing

To add a benchmark:

1. Create `benchmark_<component>.py`
2. Use the `timeit` module for timing
3. Report results in standard format
4. Add to `benchmark.sh`

## CI Integration

Benchmarks run on every release tag. Results are compared against baseline to detect regressions.

Performance regressions > 20% will fail the build.

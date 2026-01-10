# Benchmark Results

Last updated: Not yet run

## Baseline (v1.0.0)

| Benchmark | Requirements | Time | Memory |
|-----------|--------------|------|--------|
| Parse (small) | 10 | TBD | TBD |
| Parse (medium) | 50 | TBD | TBD |
| Parse (large) | 200 | TBD | TBD |
| ID Manager (small) | 10 | TBD | TBD |
| ID Manager (medium) | 50 | TBD | TBD |
| ID Manager (large) | 200 | TBD | TBD |
| Generate (small) | 10 | TBD | TBD |
| Generate (medium) | 50 | TBD | TBD |
| Generate (large) | 200 | TBD | TBD |

## ID Stability Benchmark

Measures ID stability across regenerations:

| Scenario | Expected | Result |
|----------|----------|--------|
| No changes | 100% same IDs | TBD |
| Typo fixes | 100% same IDs | TBD |
| Reordering | 100% same IDs | TBD |
| New requirement | N-1 same, 1 new | TBD |
| Major rewrite | New IDs | TBD |

## Historical Trends

Results will be tracked here as versions are released.

## Notes

- All benchmarks run on GitHub Actions (ubuntu-latest, 2 cores, 7GB RAM)
- Times are median of 5 runs
- Memory is peak RSS

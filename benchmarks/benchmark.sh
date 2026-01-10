#!/bin/bash
# Benchmark runner for spec-test-generator

set -e

echo "=== Spec Test Generator Benchmarks ==="
echo ""

# Check if installed
if ! command -v spec-test-generator &> /dev/null; then
    echo "Error: spec-test-generator not installed. Run: pip install -e ."
    exit 1
fi

# Create test PRDs if they don't exist
if [ ! -f "prds/small.md" ]; then
    echo "Generating test PRDs..."
    python generate_test_prds.py
fi

echo "Running benchmarks..."
echo ""

# Parse benchmarks
echo "=== Parse + Generate Benchmarks ==="
for size in small medium large; do
    echo -n "$size: "
    rm -f output/.idmap.json 2>/dev/null || true
    time spec-test-generator prds/$size.md --output output --json > /dev/null 2>&1
done

echo ""
echo "=== ID Stability Benchmarks ==="
for size in small medium large; do
    echo "$size:"
    # First run
    spec-test-generator prds/$size.md --output output --json > /tmp/run1.json 2>&1
    # Second run (should be same IDs)
    spec-test-generator prds/$size.md --output output --json > /tmp/run2.json 2>&1
    # Compare
    if diff -q /tmp/run1.json /tmp/run2.json > /dev/null; then
        echo "  ✓ IDs stable across regeneration"
    else
        echo "  ✗ IDs changed (unexpected)"
    fi
done

echo ""
echo "=== Memory Benchmarks ==="
# Requires: pip install memory-profiler
if command -v mprof &> /dev/null; then
    for size in small medium large; do
        echo "$size:"
        rm -f output/.idmap.json 2>/dev/null || true
        mprof run spec-test-generator prds/$size.md --output output --json > /dev/null 2>&1
        mprof peak
        rm -f mprofile_*.dat
    done
else
    echo "Install memory-profiler for memory benchmarks: pip install memory-profiler"
fi

echo ""
echo "Done."

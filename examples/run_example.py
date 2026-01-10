#!/usr/bin/env python3
"""Example usage of Spec & Test Generator."""

from pathlib import Path

from spec_test_generator import (
    CoverageAnalyzer,
    GherkinGenerator,
    SpecTestGenerator,
)


def main() -> None:
    """Run the example."""
    # Paths
    example_dir = Path(__file__).parent
    prd_path = example_dir / "sample_prd.md"
    output_dir = example_dir / "output"

    print("=" * 60)
    print("Spec & Test Generator - Example")
    print("=" * 60)

    # Initialize generator
    generator = SpecTestGenerator(
        prd_path=prd_path,
        output_dir=output_dir,
    )

    # Generate all artifacts
    print("\n1. Generating requirements and test artifacts...")
    result = generator.generate()

    print(f"   - Requirements: {len(result['requirements'])}")
    print(f"   - Test cases: {len(result['test_cases'])}")
    print(f"   - Open questions: {len(result['open_questions'])}")

    # Write artifacts
    print("\n2. Writing artifacts to disk...")
    artifacts = generator.write_artifacts(result)
    for name, path in artifacts.items():
        print(f"   - {name}: {path}")

    # Generate Gherkin features
    print("\n3. Generating Gherkin feature files...")
    gherkin = GherkinGenerator(result, output_dir)
    features = gherkin.generate()
    for name, path in features.items():
        print(f"   - {name}: {path}")

    # Analyze coverage
    print("\n4. Analyzing test coverage...")
    analyzer = CoverageAnalyzer(result)
    report = analyzer.analyze()

    print(f"   - Coverage: {report.coverage_percentage:.1f}%")
    print(f"   - Gaps: {len(report.gaps)}")

    # Write coverage report
    coverage_path = analyzer.write_report(output_dir)
    print(f"   - Report: {coverage_path}")

    print("\n" + "=" * 60)
    print("Done! Check the 'output' directory for generated artifacts.")
    print("=" * 60)


if __name__ == "__main__":
    main()

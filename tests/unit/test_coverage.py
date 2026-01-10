"""Tests for coverage analyzer."""

from pathlib import Path

from spec_test_generator.coverage import CoverageAnalyzer
from spec_test_generator.models import Priority, Requirement, TestCase, TestType


class TestCoverageAnalyzer:
    """Tests for CoverageAnalyzer class."""

    def test_full_coverage(self) -> None:
        """Test with full test coverage."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="Requirement 1",
                    priority=Priority.P0,
                    acceptance_criteria=["AC1"],
                )
            ],
            "test_cases": [
                TestCase(
                    id="TEST-0001",
                    title="Test 1",
                    test_type=TestType.E2E,
                    priority=Priority.P0,
                    requirement_ids=["REQ-0001"],
                )
            ],
        }

        analyzer = CoverageAnalyzer(result)
        report = analyzer.analyze()

        assert report.total_requirements == 1
        assert report.covered_requirements == 1
        assert report.coverage_percentage == 100.0

    def test_no_coverage(self) -> None:
        """Test with no test coverage."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="Requirement 1",
                    priority=Priority.P0,
                    acceptance_criteria=["AC1"],
                )
            ],
            "test_cases": [],
        }

        analyzer = CoverageAnalyzer(result)
        report = analyzer.analyze()

        assert report.total_requirements == 1
        assert report.covered_requirements == 0
        assert report.coverage_percentage == 0.0
        assert len(report.gaps) == 1
        assert report.gaps[0].gap_type == "no_tests"
        assert report.gaps[0].severity == "critical"

    def test_partial_coverage(self) -> None:
        """Test with partial coverage."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="Req 1",
                    priority=Priority.P0,
                    acceptance_criteria=["AC1"],
                ),
                Requirement(
                    id="REQ-0002",
                    statement="Req 2",
                    priority=Priority.P1,
                    acceptance_criteria=["AC2"],
                ),
            ],
            "test_cases": [
                TestCase(
                    id="TEST-0001",
                    title="Test 1",
                    test_type=TestType.UNIT,
                    priority=Priority.P0,
                    requirement_ids=["REQ-0001"],
                )
            ],
        }

        analyzer = CoverageAnalyzer(result)
        report = analyzer.analyze()

        assert report.coverage_percentage == 50.0
        assert len(report.gaps) >= 1  # At least the uncovered requirement

    def test_missing_e2e_for_p0(self) -> None:
        """Test detection of missing E2E tests for P0 requirements."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="Critical requirement",
                    priority=Priority.P0,
                    acceptance_criteria=["AC1"],
                )
            ],
            "test_cases": [
                TestCase(
                    id="TEST-0001",
                    title="Unit test",
                    test_type=TestType.UNIT,
                    priority=Priority.P0,
                    requirement_ids=["REQ-0001"],
                )
            ],
        }

        analyzer = CoverageAnalyzer(result)
        report = analyzer.analyze()

        e2e_gaps = [g for g in report.gaps if g.gap_type == "type_missing"]
        assert len(e2e_gaps) == 1
        assert "E2E" in e2e_gaps[0].description

    def test_report_to_markdown(self) -> None:
        """Test markdown report generation."""
        result = {"requirements": [], "test_cases": []}
        analyzer = CoverageAnalyzer(result)
        report = analyzer.analyze()

        markdown = report.to_markdown()
        assert "# Test Coverage Gap Analysis" in markdown
        assert "Coverage" in markdown

    def test_write_report(self, tmp_path: Path) -> None:
        """Test writing report to file."""
        result = {"requirements": [], "test_cases": []}
        analyzer = CoverageAnalyzer(result)

        path = analyzer.write_report(tmp_path)
        assert path.exists()
        assert "COVERAGE_REPORT.md" in str(path)

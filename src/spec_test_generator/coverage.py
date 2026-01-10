"""Test coverage gap analysis."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import Priority, Requirement, TestCase, TestType


@dataclass
class CoverageGap:
    """A gap in test coverage."""

    req_id: str
    statement: str
    priority: Priority
    gap_type: str  # "no_tests", "no_negative", "no_edge_case", "type_missing"
    description: str
    severity: str  # "critical", "high", "medium", "low"


@dataclass
class CoverageReport:
    """Test coverage analysis report."""

    total_requirements: int
    covered_requirements: int
    coverage_percentage: float
    gaps: list[CoverageGap] = field(default_factory=list)
    test_type_coverage: dict[str, int] = field(default_factory=dict)
    priority_coverage: dict[str, dict[str, int]] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            "# Test Coverage Gap Analysis",
            "",
            "## Summary",
            "",
            f"- **Total Requirements**: {self.total_requirements}",
            f"- **Covered Requirements**: {self.covered_requirements}",
            f"- **Coverage**: {self.coverage_percentage:.1f}%",
            "",
        ]

        # Test type coverage
        lines.extend(["## Coverage by Test Type", ""])
        for test_type, count in self.test_type_coverage.items():
            lines.append(f"- **{test_type}**: {count} tests")
        lines.append("")

        # Priority coverage
        lines.extend(["## Coverage by Priority", ""])
        for priority, stats in self.priority_coverage.items():
            total = stats.get("total", 0)
            covered = stats.get("covered", 0)
            pct = (covered / total * 100) if total > 0 else 0
            lines.append(f"- **{priority}**: {covered}/{total} ({pct:.0f}%)")
        lines.append("")

        # Gaps
        if self.gaps:
            lines.extend(["## Coverage Gaps", ""])

            # Group by severity
            by_severity: dict[str, list[CoverageGap]] = {}
            for gap in self.gaps:
                by_severity.setdefault(gap.severity, []).append(gap)

            for severity in ["critical", "high", "medium", "low"]:
                if severity in by_severity:
                    lines.append(f"### {severity.upper()} Severity")
                    lines.append("")
                    for gap in by_severity[severity]:
                        lines.append(f"- **{gap.req_id}** ({gap.gap_type})")
                        lines.append(f"  - {gap.description}")
                        lines.append(f"  - Statement: {gap.statement[:80]}...")
                    lines.append("")
        else:
            lines.extend(["## Coverage Gaps", "", "No coverage gaps identified!", ""])

        return "\n".join(lines)


class CoverageAnalyzer:
    """Analyzes test coverage and identifies gaps."""

    def __init__(self, result: dict[str, Any]):
        """Initialize analyzer.

        Args:
            result: Generation result with requirements and test_cases
        """
        self.result = result

    def analyze(self) -> CoverageReport:
        """Analyze test coverage and return report.

        Returns:
            Coverage report with gaps and statistics
        """
        requirements: list[Requirement] = self.result.get("requirements", [])
        test_cases: list[TestCase] = self.result.get("test_cases", [])

        # Build test lookup by requirement
        tests_by_req: dict[str, list[TestCase]] = {}
        for test in test_cases:
            for req_id in test.requirement_ids:
                tests_by_req.setdefault(req_id, []).append(test)

        # Calculate coverage
        gaps = []
        covered_reqs = set()
        test_type_counts: dict[str, int] = {}
        priority_stats: dict[str, dict[str, int]] = {}

        for req in requirements:
            priority_key = req.priority.value
            if priority_key not in priority_stats:
                priority_stats[priority_key] = {"total": 0, "covered": 0}
            priority_stats[priority_key]["total"] += 1

            req_tests = tests_by_req.get(req.id, [])

            if not req_tests:
                # No tests at all
                gaps.append(
                    CoverageGap(
                        req_id=req.id,
                        statement=req.statement,
                        priority=req.priority,
                        gap_type="no_tests",
                        description="Requirement has no test coverage",
                        severity=self._priority_to_severity(req.priority),
                    )
                )
            else:
                covered_reqs.add(req.id)
                priority_stats[priority_key]["covered"] += 1

                # Count test types
                for test in req_tests:
                    test_type_counts[test.test_type.value] = (
                        test_type_counts.get(test.test_type.value, 0) + 1
                    )

                # Check for negative tests
                has_negative = any("negative" in t.title.lower() for t in req_tests)
                if not has_negative and req.edge_cases:
                    gaps.append(
                        CoverageGap(
                            req_id=req.id,
                            statement=req.statement,
                            priority=req.priority,
                            gap_type="no_negative",
                            description="No negative/error case tests",
                            severity="medium",
                        )
                    )

                # Check test type coverage for P0 requirements
                if req.priority == Priority.P0:
                    test_types = {t.test_type for t in req_tests}
                    if TestType.E2E not in test_types:
                        gaps.append(
                            CoverageGap(
                                req_id=req.id,
                                statement=req.statement,
                                priority=req.priority,
                                gap_type="type_missing",
                                description="P0 requirement missing E2E test",
                                severity="high",
                            )
                        )

        coverage_pct = len(covered_reqs) / len(requirements) * 100 if requirements else 0

        return CoverageReport(
            total_requirements=len(requirements),
            covered_requirements=len(covered_reqs),
            coverage_percentage=coverage_pct,
            gaps=gaps,
            test_type_coverage=test_type_counts,
            priority_coverage=priority_stats,
        )

    def _priority_to_severity(self, priority: Priority) -> str:
        """Map priority to gap severity."""
        mapping = {
            Priority.P0: "critical",
            Priority.P1: "high",
            Priority.P2: "medium",
        }
        return mapping.get(priority, "low")

    def write_report(self, output_dir: Path) -> Path:
        """Write coverage report to file.

        Args:
            output_dir: Output directory

        Returns:
            Path to generated report
        """
        report = self.analyze()
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "COVERAGE_REPORT.md"
        path.write_text(report.to_markdown())
        return path

"""Output artifact generators."""

from pathlib import Path
from typing import Any

from .models import PolicyConfig, Requirement, TestCase, TestPlan, TraceabilityEntry


class OutputGenerator:
    """Generates spec and test output artifacts."""

    def __init__(
        self,
        result: dict[str, Any],
        policy: PolicyConfig,
        output_dir: Path,
    ):
        """Initialize output generator."""
        self.result = result
        self.policy = policy
        self.output_dir = output_dir

    def generate_all(self) -> dict[str, Path]:
        """Generate all artifacts."""
        artifacts = {}

        artifacts["REQUIREMENTS.md"] = self._generate_requirements()
        artifacts["TEST_PLAN.md"] = self._generate_test_plan()
        artifacts["TEST_CASES.md"] = self._generate_test_cases()
        artifacts["TRACEABILITY.csv"] = self._generate_traceability()

        return artifacts

    def _generate_requirements(self) -> Path:
        """Generate REQUIREMENTS.md."""
        requirements: list[Requirement] = self.result["requirements"]
        open_questions: list[str] = self.result.get("open_questions", [])
        assumptions: list[str] = self.result.get("assumptions", [])

        lines = ["# Requirements", ""]

        # Assumptions section
        if assumptions:
            lines.extend(["## Assumptions"])
            for assumption in assumptions:
                lines.append(f"- {assumption}")
            lines.append("")

        # Open questions section
        if open_questions:
            lines.extend(["## Open Questions"])
            for question in open_questions:
                lines.append(f"- {question}")
            lines.append("")

        # Group requirements by feature area
        by_area: dict[str, list[Requirement]] = {}
        for req in requirements:
            area = req.feature_area or "General"
            by_area.setdefault(area, []).append(req)

        for area, reqs in by_area.items():
            lines.extend([f"## Feature: {area}", ""])
            for req in reqs:
                lines.append(req.to_markdown())
                lines.append("")

        content = "\n".join(lines)
        path = self.output_dir / "REQUIREMENTS.md"
        path.write_text(content)
        return path

    def _generate_test_plan(self) -> Path:
        """Generate TEST_PLAN.md."""
        test_plan: TestPlan = self.result["test_plan"]

        content = test_plan.to_markdown()
        path = self.output_dir / "TEST_PLAN.md"
        path.write_text(content)
        return path

    def _generate_test_cases(self) -> Path:
        """Generate TEST_CASES.md."""
        test_cases: list[TestCase] = self.result["test_cases"]

        lines = ["# Test Cases", ""]

        for test in test_cases:
            lines.append(test.to_markdown())
            lines.append("")

        content = "\n".join(lines)
        path = self.output_dir / "TEST_CASES.md"
        path.write_text(content)
        return path

    def _generate_traceability(self) -> Path:
        """Generate TRACEABILITY.csv."""
        entries: list[TraceabilityEntry] = self.result["traceability"]

        lines = ["REQ_ID,TEST_ID,TYPE,PRIORITY"]
        for entry in entries:
            lines.append(entry.to_csv_row())

        content = "\n".join(lines)
        path = self.output_dir / "TRACEABILITY.csv"
        path.write_text(content)
        return path

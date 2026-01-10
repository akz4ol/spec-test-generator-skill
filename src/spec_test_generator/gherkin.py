"""Gherkin/BDD output generator."""

from pathlib import Path
from typing import Any

from .models import Requirement, TestCase


class GherkinGenerator:
    """Generates Gherkin .feature files from requirements and test cases."""

    def __init__(self, result: dict[str, Any], output_dir: Path):
        """Initialize Gherkin generator.

        Args:
            result: Generation result with requirements and test_cases
            output_dir: Directory for output files
        """
        self.result = result
        self.output_dir = output_dir

    def generate(self) -> dict[str, Path]:
        """Generate all Gherkin feature files.

        Returns:
            Dict mapping feature names to file paths
        """
        artifacts: dict[str, Path] = {}

        # Group requirements by feature area
        by_area: dict[str, list[Requirement]] = {}
        for req in self.result.get("requirements", []):
            area = req.feature_area or "General"
            by_area.setdefault(area, []).append(req)

        # Create test case lookup by requirement ID
        test_lookup: dict[str, list[TestCase]] = {}
        for test in self.result.get("test_cases", []):
            for req_id in test.requirement_ids:
                test_lookup.setdefault(req_id, []).append(test)

        # Generate feature file per area
        for area, requirements in by_area.items():
            feature_content = self._generate_feature(area, requirements, test_lookup)
            filename = self._sanitize_filename(area) + ".feature"
            path = self.output_dir / "features" / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(feature_content)
            artifacts[filename] = path

        return artifacts

    def _generate_feature(
        self,
        area: str,
        requirements: list[Requirement],
        test_lookup: dict[str, list[TestCase]],
    ) -> str:
        """Generate a single feature file."""
        lines = [
            f"Feature: {area}",
            "  As a user",
            f"  I want {area.lower()} functionality",
            "  So that the system meets requirements",
            "",
        ]

        for req in requirements:
            lines.extend(self._generate_scenarios(req, test_lookup.get(req.id, [])))

        return "\n".join(lines)

    def _generate_scenarios(self, req: Requirement, test_cases: list[TestCase]) -> list[str]:
        """Generate Gherkin scenarios for a requirement."""
        lines = []

        # Add requirement as a background comment
        lines.append(f"  # {req.id}: {req.statement}")
        lines.append(f"  @{req.id} @{req.priority.value}")
        lines.append("")

        if test_cases:
            # Generate scenarios from test cases
            for test in test_cases:
                lines.extend(self._test_to_scenario(test))
                lines.append("")
        else:
            # Generate basic scenario from acceptance criteria
            lines.extend(self._req_to_scenario(req))
            lines.append("")

        return lines

    def _test_to_scenario(self, test: TestCase) -> list[str]:
        """Convert a test case to a Gherkin scenario."""
        lines = [f"  Scenario: {test.title}"]

        # Generate Given from preconditions
        if test.preconditions:
            lines.append(f"    Given {test.preconditions}")
        else:
            lines.append("    Given the system is in a valid state")

        # Generate When from steps
        for i, step in enumerate(test.steps):
            keyword = "When" if i == 0 else "And"
            lines.append(f"    {keyword} {step.lower()}")

        # Generate Then from expected
        for i, exp in enumerate(test.expected):
            keyword = "Then" if i == 0 else "And"
            lines.append(f"    {keyword} {exp.lower()}")

        return lines

    def _req_to_scenario(self, req: Requirement) -> list[str]:
        """Convert a requirement to a basic Gherkin scenario."""
        lines = [f"  Scenario: Verify {req.id}"]

        # Parse acceptance criteria into Given/When/Then
        for i, ac in enumerate(req.acceptance_criteria):
            ac_lower = ac.lower()
            if "given" in ac_lower and "when" in ac_lower and "then" in ac_lower:
                # Already in Gherkin format, parse it
                lines.extend(self._parse_gherkin_ac(ac))
            else:
                # Generate basic scenario
                if i == 0:
                    lines.append("    Given the system is ready")
                    lines.append("    When the user performs the action")
                    lines.append(f"    Then {ac.lower()}")
                else:
                    lines.append(f"    And {ac.lower()}")

        return lines

    def _parse_gherkin_ac(self, ac: str) -> list[str]:
        """Parse acceptance criteria that's already in Gherkin format."""
        lines = []
        ac_lower = ac.lower()

        # Extract Given
        given_start = ac_lower.find("given")
        when_start = ac_lower.find("when")
        then_start = ac_lower.find("then")

        if given_start != -1 and when_start != -1:
            given_text = ac[given_start + 6 : when_start].strip().rstrip(",")
            lines.append(f"    Given {given_text}")

        if when_start != -1 and then_start != -1:
            when_text = ac[when_start + 5 : then_start].strip().rstrip(",")
            lines.append(f"    When {when_text}")

        if then_start != -1:
            then_text = ac[then_start + 5 :].strip()
            lines.append(f"    Then {then_text}")

        return lines if lines else ["    Given the scenario is defined", f"    Then {ac}"]

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize string for use as filename."""
        return name.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace(":", "")

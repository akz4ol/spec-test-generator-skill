"""Change impact analysis between PRD versions."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .id_manager import IDManager
from .parser import PRDParser


@dataclass
class Change:
    """A detected change between versions."""

    change_type: str  # "added", "removed", "modified", "priority_changed"
    req_id: str | None
    description: str
    impact: str
    old_value: str | None = None
    new_value: str | None = None


@dataclass
class ImpactReport:
    """Change impact analysis report."""

    baseline_version: str
    current_version: str
    changes: list[Change] = field(default_factory=list)
    affected_tests: list[str] = field(default_factory=list)
    risk_level: str = "low"  # "low", "medium", "high", "critical"

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            "# Change Impact Report",
            "",
            f"**Baseline**: {self.baseline_version}",
            f"**Current**: {self.current_version}",
            f"**Risk Level**: {self.risk_level.upper()}",
            "",
            "## Summary",
            "",
            f"- **Total Changes**: {len(self.changes)}",
            f"- **Added Requirements**: {sum(1 for c in self.changes if c.change_type == 'added')}",
            f"- **Removed Requirements**: {sum(1 for c in self.changes if c.change_type == 'removed')}",
            f"- **Modified Requirements**: {sum(1 for c in self.changes if c.change_type == 'modified')}",
            f"- **Affected Tests**: {len(self.affected_tests)}",
            "",
        ]

        # Group changes by type
        if self.changes:
            lines.extend(["## Changes", ""])

            # Removed (most impactful first)
            removed = [c for c in self.changes if c.change_type == "removed"]
            if removed:
                lines.append("### Removed Requirements")
                lines.append("")
                for change in removed:
                    lines.append(f"- **{change.req_id}**: {change.description}")
                    lines.append(f"  - Impact: {change.impact}")
                lines.append("")

            # Added
            added = [c for c in self.changes if c.change_type == "added"]
            if added:
                lines.append("### Added Requirements")
                lines.append("")
                for change in added:
                    lines.append(f"- **{change.req_id}**: {change.description}")
                    lines.append(f"  - Impact: {change.impact}")
                lines.append("")

            # Modified
            modified = [c for c in self.changes if c.change_type == "modified"]
            if modified:
                lines.append("### Modified Requirements")
                lines.append("")
                for change in modified:
                    lines.append(f"- **{change.req_id}**: {change.description}")
                    if change.old_value and change.new_value:
                        lines.append(f"  - Old: {change.old_value[:100]}...")
                        lines.append(f"  - New: {change.new_value[:100]}...")
                    lines.append(f"  - Impact: {change.impact}")
                lines.append("")

            # Priority changes
            priority_changes = [c for c in self.changes if c.change_type == "priority_changed"]
            if priority_changes:
                lines.append("### Priority Changes")
                lines.append("")
                for change in priority_changes:
                    lines.append(f"- **{change.req_id}**: {change.old_value} → {change.new_value}")
                    lines.append(f"  - Impact: {change.impact}")
                lines.append("")

        # Affected tests
        if self.affected_tests:
            lines.extend(["## Affected Tests", ""])
            for test_id in self.affected_tests:
                lines.append(f"- {test_id}")
            lines.append("")

        # Recommendations
        lines.extend(["## Recommendations", ""])
        if self.risk_level in ("high", "critical"):
            lines.append("- Review all removed requirements with stakeholders")
            lines.append("- Update or remove associated test cases")
            lines.append("- Update documentation and release notes")
        elif self.risk_level == "medium":
            lines.append("- Review modified requirements for test impact")
            lines.append("- Add tests for new requirements")
        else:
            lines.append("- Standard review process recommended")
        lines.append("")

        return "\n".join(lines)


class ImpactAnalyzer:
    """Analyzes changes between PRD versions."""

    def __init__(self, output_dir: Path):
        """Initialize analyzer.

        Args:
            output_dir: Output directory for ID management
        """
        self.output_dir = output_dir
        self.id_manager = IDManager(output_dir)

    def compare(
        self,
        baseline_path: str | Path,
        current_path: str | Path,
        existing_tests: list[dict[str, Any]] | None = None,
    ) -> ImpactReport:
        """Compare two PRD versions and generate impact report.

        Args:
            baseline_path: Path to baseline PRD
            current_path: Path to current PRD
            existing_tests: Optional list of existing test case dicts

        Returns:
            Impact analysis report
        """
        # Parse both PRDs
        baseline_parser = PRDParser(baseline_path)
        current_parser = PRDParser(current_path)

        baseline_prd = baseline_parser.parse()
        current_prd = current_parser.parse()

        # Generate requirements from both
        baseline_reqs = self._extract_requirements(baseline_prd.functional_requirements)
        current_reqs = self._extract_requirements(current_prd.functional_requirements)

        # Build lookup maps
        baseline_map = {r["hash"]: r for r in baseline_reqs}
        current_map = {r["hash"]: r for r in current_reqs}

        changes: list[Change] = []
        affected_tests: list[str] = []

        # Find removed requirements
        for hash_key, req in baseline_map.items():
            if hash_key not in current_map:
                changes.append(
                    Change(
                        change_type="removed",
                        req_id=req["id"],
                        description=f"Requirement removed: {req['statement'][:60]}...",
                        impact="Existing tests for this requirement should be reviewed/removed",
                        old_value=req["statement"],
                    )
                )
                # Find affected tests
                if existing_tests:
                    for test in existing_tests:
                        if req["id"] in test.get("requirement_ids", []):
                            affected_tests.append(test.get("id", "Unknown"))

        # Find added requirements
        for hash_key, req in current_map.items():
            if hash_key not in baseline_map:
                changes.append(
                    Change(
                        change_type="added",
                        req_id=req["id"],
                        description=f"New requirement: {req['statement'][:60]}...",
                        impact="New tests should be created for this requirement",
                        new_value=req["statement"],
                    )
                )

        # Find modified requirements (same ID but different content)
        for hash_key, current_req in current_map.items():
            if hash_key in baseline_map:
                baseline_req = baseline_map[hash_key]
                # Check for statement changes beyond hash match
                if baseline_req["statement"] != current_req["statement"]:
                    changes.append(
                        Change(
                            change_type="modified",
                            req_id=current_req["id"],
                            description="Requirement statement modified",
                            impact="Review associated tests for accuracy",
                            old_value=baseline_req["statement"],
                            new_value=current_req["statement"],
                        )
                    )
                    if existing_tests:
                        for test in existing_tests:
                            if current_req["id"] in test.get("requirement_ids", []):
                                affected_tests.append(test.get("id", "Unknown"))

        # Determine risk level
        risk_level = self._calculate_risk(changes)

        return ImpactReport(
            baseline_version=str(baseline_path),
            current_version=str(current_path),
            changes=changes,
            affected_tests=list(set(affected_tests)),
            risk_level=risk_level,
        )

    def _extract_requirements(self, req_texts: list[str]) -> list[dict[str, Any]]:
        """Extract requirement info from PRD requirement texts."""
        requirements = []
        for text in req_texts:
            hash_key = self.id_manager.hash_statement(text)
            req_id = self.id_manager.get_requirement_id(hash_key)
            requirements.append(
                {
                    "hash": hash_key,
                    "id": req_id,
                    "statement": text,
                }
            )
        return requirements

    def _calculate_risk(self, changes: list[Change]) -> str:
        """Calculate overall risk level from changes."""
        removed_count = sum(1 for c in changes if c.change_type == "removed")
        modified_count = sum(1 for c in changes if c.change_type == "modified")

        if removed_count >= 3 or (removed_count >= 1 and modified_count >= 3):
            return "critical"
        elif removed_count >= 1 or modified_count >= 3:
            return "high"
        elif modified_count >= 1 or len(changes) >= 3:
            return "medium"
        else:
            return "low"

    def write_report(
        self,
        baseline_path: str | Path,
        current_path: str | Path,
        existing_tests: list[dict[str, Any]] | None = None,
    ) -> Path:
        """Generate and write impact report to file.

        Args:
            baseline_path: Path to baseline PRD
            current_path: Path to current PRD
            existing_tests: Optional list of existing test case dicts

        Returns:
            Path to generated report
        """
        report = self.compare(baseline_path, current_path, existing_tests)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / "IMPACT_REPORT.md"
        path.write_text(report.to_markdown())
        return path

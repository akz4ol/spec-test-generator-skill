"""Tests for impact analyzer."""

from pathlib import Path

from spec_test_generator.impact import ImpactAnalyzer


class TestImpactAnalyzer:
    """Tests for ImpactAnalyzer class."""

    def test_detect_added_requirement(self, tmp_path: Path) -> None:
        """Test detecting added requirements."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("""
# PRD v1

## Functional Requirements
1) Requirement A
""")

        current = tmp_path / "current.md"
        current.write_text("""
# PRD v2

## Functional Requirements
1) Requirement A
2) Requirement B
""")

        analyzer = ImpactAnalyzer(tmp_path)
        report = analyzer.compare(baseline, current)

        added = [c for c in report.changes if c.change_type == "added"]
        assert len(added) == 1
        assert "Requirement B" in added[0].new_value

    def test_detect_removed_requirement(self, tmp_path: Path) -> None:
        """Test detecting removed requirements."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("""
# PRD v1

## Functional Requirements
1) Requirement A
2) Requirement B
""")

        current = tmp_path / "current.md"
        current.write_text("""
# PRD v2

## Functional Requirements
1) Requirement A
""")

        analyzer = ImpactAnalyzer(tmp_path)
        report = analyzer.compare(baseline, current)

        removed = [c for c in report.changes if c.change_type == "removed"]
        assert len(removed) == 1
        assert "Requirement B" in removed[0].old_value

    def test_no_changes(self, tmp_path: Path) -> None:
        """Test with no changes between versions."""
        prd_content = """
# PRD

## Functional Requirements
1) Same requirement
"""
        baseline = tmp_path / "baseline.md"
        baseline.write_text(prd_content)

        current = tmp_path / "current.md"
        current.write_text(prd_content)

        analyzer = ImpactAnalyzer(tmp_path)
        report = analyzer.compare(baseline, current)

        assert len(report.changes) == 0
        assert report.risk_level == "low"

    def test_risk_level_calculation(self, tmp_path: Path) -> None:
        """Test risk level is calculated correctly."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("""
# PRD

## Functional Requirements
1) Req A
2) Req B
3) Req C
4) Req D
""")

        current = tmp_path / "current.md"
        current.write_text("""
# PRD

## Functional Requirements
1) Req A
""")

        analyzer = ImpactAnalyzer(tmp_path)
        report = analyzer.compare(baseline, current)

        # 3 removed requirements should be critical
        assert report.risk_level == "critical"

    def test_affected_tests(self, tmp_path: Path) -> None:
        """Test that affected tests are identified."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("""
# PRD

## Functional Requirements
1) User authentication
""")

        current = tmp_path / "current.md"
        current.write_text("""
# PRD

## Functional Requirements
1) Different requirement
""")

        # First run to get the requirement ID
        analyzer = ImpactAnalyzer(tmp_path)
        _ = analyzer.compare(baseline, baseline)  # Generate IDs

        # Get the ID that was assigned
        from spec_test_generator.id_manager import IDManager

        id_mgr = IDManager(tmp_path)
        req_hash = id_mgr.hash_statement("User authentication")
        req_id = id_mgr.get_requirement_id(req_hash)

        existing_tests = [{"id": "TEST-0001", "requirement_ids": [req_id]}]

        report = analyzer.compare(baseline, current, existing_tests)

        assert "TEST-0001" in report.affected_tests

    def test_report_to_markdown(self, tmp_path: Path) -> None:
        """Test markdown report generation."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("# PRD\n\n## Functional Requirements\n1) Req A")

        current = tmp_path / "current.md"
        current.write_text("# PRD\n\n## Functional Requirements\n1) Req B")

        analyzer = ImpactAnalyzer(tmp_path)
        report = analyzer.compare(baseline, current)

        markdown = report.to_markdown()
        assert "# Change Impact Report" in markdown
        assert "Risk Level" in markdown

    def test_write_report(self, tmp_path: Path) -> None:
        """Test writing report to file."""
        baseline = tmp_path / "baseline.md"
        baseline.write_text("# PRD\n\n## Functional Requirements\n1) Req")

        current = tmp_path / "current.md"
        current.write_text("# PRD\n\n## Functional Requirements\n1) Req")

        analyzer = ImpactAnalyzer(tmp_path)
        path = analyzer.write_report(baseline, current)

        assert path.exists()
        assert "IMPACT_REPORT.md" in str(path)

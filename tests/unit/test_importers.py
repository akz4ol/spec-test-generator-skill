"""Tests for importers."""

import json
from pathlib import Path

from spec_test_generator.id_manager import IDManager
from spec_test_generator.importers import JiraImporter, LinearImporter
from spec_test_generator.models import Priority


class TestJiraImporter:
    """Tests for JiraImporter class."""

    def test_import_single_issue(self, tmp_path: Path) -> None:
        """Test importing a single Jira issue."""
        jira_data = {
            "issues": [
                {
                    "key": "PROJ-123",
                    "fields": {
                        "summary": "Implement user login",
                        "description": "Users should be able to log in",
                        "priority": {"name": "High"},
                        "labels": ["authentication"],
                    },
                }
            ]
        }

        export_file = tmp_path / "jira_export.json"
        export_file.write_text(json.dumps(jira_data))

        id_manager = IDManager(tmp_path)
        importer = JiraImporter(id_manager)
        requirements = importer.import_from_file(export_file)

        assert len(requirements) == 1
        assert "implement user login" in requirements[0].statement.lower()
        assert requirements[0].priority == Priority.P1
        assert requirements[0].feature_area == "authentication"

    def test_import_with_acceptance_criteria(self, tmp_path: Path) -> None:
        """Test extracting acceptance criteria from description."""
        jira_data = {
            "issues": [
                {
                    "fields": {
                        "summary": "Add search feature",
                        "description": "## Acceptance Criteria\n- Search by name\n- Search by email\n\n## Notes\nOther stuff",
                        "priority": {"name": "Medium"},
                    }
                }
            ]
        }

        export_file = tmp_path / "jira_export.json"
        export_file.write_text(json.dumps(jira_data))

        id_manager = IDManager(tmp_path)
        importer = JiraImporter(id_manager)
        requirements = importer.import_from_file(export_file)

        assert len(requirements) == 1
        assert "Search by name" in requirements[0].acceptance_criteria

    def test_priority_mapping(self, tmp_path: Path) -> None:
        """Test Jira priority mapping."""
        id_manager = IDManager(tmp_path)
        importer = JiraImporter(id_manager)

        assert importer._map_priority({"name": "Highest"}) == Priority.P0
        assert importer._map_priority({"name": "High"}) == Priority.P1
        assert importer._map_priority({"name": "Low"}) == Priority.P2


class TestLinearImporter:
    """Tests for LinearImporter class."""

    def test_import_single_issue(self, tmp_path: Path) -> None:
        """Test importing a single Linear issue."""
        linear_data = {
            "issues": [
                {
                    "title": "Implement dashboard",
                    "description": "Create main dashboard view",
                    "priority": 2,
                    "project": {"name": "Frontend"},
                }
            ]
        }

        export_file = tmp_path / "linear_export.json"
        export_file.write_text(json.dumps(linear_data))

        id_manager = IDManager(tmp_path)
        importer = LinearImporter(id_manager)
        requirements = importer.import_from_file(export_file)

        assert len(requirements) == 1
        assert "implement dashboard" in requirements[0].statement.lower()
        assert requirements[0].priority == Priority.P1
        assert requirements[0].feature_area == "Frontend"

    def test_priority_mapping(self, tmp_path: Path) -> None:
        """Test Linear priority mapping."""
        id_manager = IDManager(tmp_path)
        importer = LinearImporter(id_manager)

        assert importer._map_priority(1) == Priority.P0  # Urgent
        assert importer._map_priority(2) == Priority.P1  # High
        assert importer._map_priority(4) == Priority.P2  # Low

"""Import from external systems (Jira, Linear)."""

import json
from pathlib import Path
from typing import Any

from .id_manager import IDManager
from .models import Priority, Requirement


class JiraImporter:
    """Import requirements from Jira JSON export."""

    def __init__(self, id_manager: IDManager):
        """Initialize importer.

        Args:
            id_manager: ID manager for stable IDs
        """
        self.id_manager = id_manager

    def import_from_file(self, path: str | Path) -> list[Requirement]:
        """Import requirements from Jira JSON export file.

        Args:
            path: Path to Jira JSON export

        Returns:
            List of imported requirements
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Jira export file not found: {path}")

        with open(path) as f:
            data = json.load(f)

        return self.import_from_dict(data)

    def import_from_dict(self, data: dict[str, Any]) -> list[Requirement]:
        """Import requirements from Jira JSON data.

        Args:
            data: Jira JSON export data

        Returns:
            List of imported requirements
        """
        requirements = []

        # Handle Jira JSON export format
        issues = data.get("issues", [data] if "key" in data else [])

        for issue in issues:
            req = self._parse_issue(issue)
            if req:
                requirements.append(req)

        return requirements

    def _parse_issue(self, issue: dict[str, Any]) -> Requirement | None:
        """Parse a single Jira issue into a requirement."""
        fields = issue.get("fields", issue)

        # Extract summary/title
        summary = fields.get("summary", "")
        if not summary:
            return None

        # Extract description
        description = fields.get("description", "")
        if isinstance(description, dict):
            # Handle Atlassian Document Format
            description = self._parse_adf(description)

        # Generate statement
        statement = f"The system SHALL {summary.lower()}"

        # Get stable ID
        statement_hash = self.id_manager.hash_statement(statement)
        req_id = self.id_manager.get_requirement_id(statement_hash)

        # Map priority
        priority = self._map_priority(fields.get("priority", {}))

        # Extract acceptance criteria from description or custom field
        acceptance_criteria = self._extract_acceptance_criteria(description, fields)

        # Extract labels as feature area
        labels = fields.get("labels", [])
        feature_area = labels[0] if labels else fields.get("project", {}).get("name", "Imported")

        return Requirement(
            id=req_id,
            statement=statement,
            priority=priority,
            acceptance_criteria=acceptance_criteria,
            edge_cases=[],
            rationale=description[:200] if description else None,
            feature_area=feature_area,
        )

    def _map_priority(self, priority_field: dict[str, Any] | str) -> Priority:
        """Map Jira priority to internal priority."""
        if isinstance(priority_field, str):
            name = priority_field.lower()
        else:
            name = priority_field.get("name", "").lower()

        if name in ("highest", "blocker", "critical"):
            return Priority.P0
        elif name in ("high", "major"):
            return Priority.P1
        else:
            return Priority.P2

    def _extract_acceptance_criteria(self, description: str, fields: dict[str, Any]) -> list[str]:
        """Extract acceptance criteria from description or custom field."""
        criteria = []

        # Check for custom acceptance criteria field
        for key, value in fields.items():
            if "acceptance" in key.lower() and isinstance(value, str):
                for line in value.split("\n"):
                    line = line.strip().lstrip("-*• ")
                    if line:
                        criteria.append(line)

        # Parse from description if none found
        if not criteria and description:
            in_ac_section = False
            for line in description.split("\n"):
                line_lower = line.lower().strip()
                if "acceptance" in line_lower and "criteria" in line_lower:
                    in_ac_section = True
                    continue
                elif in_ac_section:
                    if line.startswith("#") or (
                        line.strip() and not line.startswith(("-", "*", "•", " "))
                    ):
                        in_ac_section = False
                    else:
                        cleaned = line.strip().lstrip("-*• ")
                        if cleaned:
                            criteria.append(cleaned)

        return criteria if criteria else ["Verify requirement is met"]

    def _parse_adf(self, doc: dict[str, Any]) -> str:
        """Parse Atlassian Document Format to plain text."""
        text_parts = []

        def extract_text(node: dict[str, Any]) -> None:
            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))
            for child in node.get("content", []):
                extract_text(child)

        extract_text(doc)
        return "\n".join(text_parts)


class LinearImporter:
    """Import requirements from Linear JSON export."""

    def __init__(self, id_manager: IDManager):
        """Initialize importer.

        Args:
            id_manager: ID manager for stable IDs
        """
        self.id_manager = id_manager

    def import_from_file(self, path: str | Path) -> list[Requirement]:
        """Import requirements from Linear JSON export file.

        Args:
            path: Path to Linear JSON export

        Returns:
            List of imported requirements
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Linear export file not found: {path}")

        with open(path) as f:
            data = json.load(f)

        return self.import_from_dict(data)

    def import_from_dict(self, data: dict[str, Any]) -> list[Requirement]:
        """Import requirements from Linear JSON data.

        Args:
            data: Linear JSON export data

        Returns:
            List of imported requirements
        """
        requirements = []

        # Handle Linear JSON export format
        issues = data.get("issues", data.get("data", {}).get("issues", {}).get("nodes", []))
        if isinstance(issues, dict):
            issues = issues.get("nodes", [])

        for issue in issues:
            req = self._parse_issue(issue)
            if req:
                requirements.append(req)

        return requirements

    def _parse_issue(self, issue: dict[str, Any]) -> Requirement | None:
        """Parse a single Linear issue into a requirement."""
        # Extract title
        title = issue.get("title", "")
        if not title:
            return None

        # Extract description
        description = issue.get("description", "") or ""

        # Generate statement
        statement = f"The system SHALL {title.lower()}"

        # Get stable ID
        statement_hash = self.id_manager.hash_statement(statement)
        req_id = self.id_manager.get_requirement_id(statement_hash)

        # Map priority
        priority = self._map_priority(issue.get("priority", 0))

        # Extract acceptance criteria
        acceptance_criteria = self._extract_acceptance_criteria(description)

        # Get project/team as feature area
        project = issue.get("project", {}) or {}
        team = issue.get("team", {}) or {}
        feature_area = project.get("name", team.get("name", "Imported"))

        # Get labels
        labels = issue.get("labels", {})
        if isinstance(labels, dict):
            label_nodes = labels.get("nodes", [])
            if label_nodes:
                feature_area = label_nodes[0].get("name", feature_area)

        return Requirement(
            id=req_id,
            statement=statement,
            priority=priority,
            acceptance_criteria=acceptance_criteria,
            edge_cases=[],
            rationale=description[:200] if description else None,
            feature_area=feature_area,
        )

    def _map_priority(self, priority: int | str) -> Priority:
        """Map Linear priority to internal priority."""
        if isinstance(priority, str):
            priority = int(priority) if priority.isdigit() else 3

        # Linear: 0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low
        if priority <= 1:
            return Priority.P0
        elif priority == 2:
            return Priority.P1
        else:
            return Priority.P2

    def _extract_acceptance_criteria(self, description: str) -> list[str]:
        """Extract acceptance criteria from description."""
        criteria = []

        if not description:
            return ["Verify requirement is met"]

        in_ac_section = False
        for line in description.split("\n"):
            line_lower = line.lower().strip()
            if "acceptance" in line_lower and "criteria" in line_lower:
                in_ac_section = True
                continue
            elif in_ac_section:
                if line.startswith("#") or (
                    line.strip() and not line.startswith(("-", "*", "•", " ", "["))
                ):
                    in_ac_section = False
                else:
                    # Handle markdown checkboxes
                    cleaned = line.strip().lstrip("-*•[] x")
                    if cleaned:
                        criteria.append(cleaned)

        return criteria if criteria else ["Verify requirement is met"]

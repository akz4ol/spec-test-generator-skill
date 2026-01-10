"""Data models for Spec & Test Generator."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Priority(Enum):
    """Requirement/test priority levels."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class TestType(Enum):
    """Test type categories."""

    UNIT = "Unit"
    INTEGRATION = "Integration"
    E2E = "E2E"


@dataclass
class Requirement:
    """A requirement with stable ID."""

    id: str
    statement: str
    priority: Priority
    acceptance_criteria: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    rationale: str | None = None
    notes: str | None = None
    feature_area: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "statement": self.statement,
            "priority": self.priority.value,
            "acceptance_criteria": self.acceptance_criteria,
            "edge_cases": self.edge_cases,
            "rationale": self.rationale,
            "notes": self.notes,
            "feature_area": self.feature_area,
        }

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"### {self.id} ({self.priority.value}) — {self._title()}",
            f"**Statement:** {self.statement}",
        ]

        if self.rationale:
            lines.append(f"**Rationale:** {self.rationale}")

        lines.append("**Acceptance Criteria:**")
        for ac in self.acceptance_criteria:
            lines.append(f"- {ac}")

        if self.edge_cases:
            lines.append("")
            lines.append("**Edge Cases:**")
            for ec in self.edge_cases:
                lines.append(f"- {ec}")

        if self.notes:
            lines.append("")
            lines.append(f"**Notes:** {self.notes}")

        return "\n".join(lines)

    def _title(self) -> str:
        """Generate a short title from statement."""
        words = self.statement.split()[:6]
        title = " ".join(words)
        if len(self.statement.split()) > 6:
            title += "..."
        return title


@dataclass
class TestCase:
    """A test case with stable ID."""

    id: str
    title: str
    test_type: TestType
    priority: Priority
    requirement_ids: list[str]
    preconditions: str | None = None
    steps: list[str] = field(default_factory=list)
    expected: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "test_type": self.test_type.value,
            "priority": self.priority.value,
            "requirement_ids": self.requirement_ids,
            "preconditions": self.preconditions,
            "steps": self.steps,
            "expected": self.expected,
        }

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"### {self.id} ({self.test_type.value}, {self.priority.value}) — {self.title}",
            f"**Requirements:** {', '.join(self.requirement_ids)}",
        ]

        if self.preconditions:
            lines.append(f"**Preconditions:** {self.preconditions}")

        lines.append("**Steps:**")
        for i, step in enumerate(self.steps, 1):
            lines.append(f"{i}. {step}")

        lines.append("**Expected:**")
        for exp in self.expected:
            lines.append(f"- {exp}")

        return "\n".join(lines)


@dataclass
class TestPlan:
    """Test plan strategy."""

    strategy: dict[str, str] = field(default_factory=dict)
    test_data: list[str] = field(default_factory=list)
    environments: dict[str, str] = field(default_factory=dict)
    non_functional: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = ["# Test Plan", "", "## Strategy"]

        for test_type, description in self.strategy.items():
            lines.append(f"- **{test_type}**: {description}")

        lines.extend(["", "## Test Data"])
        for item in self.test_data:
            lines.append(f"- {item}")

        lines.extend(["", "## Environments"])
        for env, description in self.environments.items():
            lines.append(f"- **{env}**: {description}")

        if self.non_functional:
            lines.extend(["", "## Non-Functional Tests"])
            for item in self.non_functional:
                lines.append(f"- {item}")

        return "\n".join(lines)


@dataclass
class TraceabilityEntry:
    """Traceability matrix entry."""

    req_id: str
    test_id: str
    test_type: TestType
    priority: Priority

    def to_csv_row(self) -> str:
        """Convert to CSV row."""
        return f"{self.req_id},{self.test_id},{self.test_type.value},{self.priority.value}"


@dataclass
class PolicyConfig:
    """Policy configuration."""

    name: str
    version: str
    config: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PolicyConfig":
        """Create from dictionary."""
        return cls(
            name=data.get("policy_name", "Unknown"),
            version=data.get("policy_version", "0.0"),
            config=data,
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot-notation key."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

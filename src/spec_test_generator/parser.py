"""PRD and input document parser."""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParsedPRD:
    """Parsed PRD structure."""

    title: str = ""
    goal: str = ""
    functional_requirements: list[str] = field(default_factory=list)
    non_functional_requirements: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    raw_content: str = ""


class PRDParser:
    """Parser for PRD markdown documents."""

    def __init__(self, prd_path: str | Path):
        """Initialize parser with PRD path."""
        self.prd_path = Path(prd_path)
        self._parsed: ParsedPRD | None = None

    def parse(self) -> ParsedPRD:
        """Parse the PRD file."""
        if self._parsed is not None:
            return self._parsed

        if not self.prd_path.exists():
            raise FileNotFoundError(f"PRD file not found: {self.prd_path}")

        content = self.prd_path.read_text()
        self._parsed = self._parse_content(content)
        return self._parsed

    def _parse_content(self, content: str) -> ParsedPRD:
        """Parse PRD markdown content."""
        result = ParsedPRD(raw_content=content)

        # Extract title from first H1
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            result.title = title_match.group(1).strip()

        # Split into sections
        sections = self._split_sections(content)

        for section_name, section_content in sections.items():
            section_lower = section_name.lower()

            if (
                "goal" in section_lower or "objective" in section_lower
            ) and "non" not in section_lower:
                result.goal = section_content.strip()

            elif "functional" in section_lower and "non" not in section_lower:
                result.functional_requirements = self._extract_list_items(section_content)

            elif "non-functional" in section_lower or "nfr" in section_lower:
                result.non_functional_requirements = self._extract_list_items(section_content)

            elif "non-goal" in section_lower or "out of scope" in section_lower:
                result.non_goals = self._extract_list_items(section_content)

            elif "note" in section_lower:
                result.notes = self._extract_list_items(section_content)

            elif "assumption" in section_lower:
                result.assumptions = self._extract_list_items(section_content)

            elif "requirement" in section_lower:
                # Generic requirements section
                items = self._extract_list_items(section_content)
                result.functional_requirements.extend(items)

        return result

    def _split_sections(self, content: str) -> dict[str, str]:
        """Split content into sections by headers."""
        sections: dict[str, str] = {}
        current_section = "preamble"
        current_content: list[str] = []

        for line in content.split("\n"):
            header_match = re.match(r"^##\s+(.+)$", line)
            if header_match:
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = header_match.group(1).strip()
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            sections[current_section] = "\n".join(current_content)

        return sections

    def _extract_list_items(self, content: str) -> list[str]:
        """Extract list items from content."""
        items = []

        # Match numbered lists: 1) item or 1. item
        numbered_pattern = r"^\s*\d+[.)]\s*(.+)$"

        # Match bullet lists: - item or * item
        bullet_pattern = r"^\s*[-*]\s+(.+)$"

        for line in content.split("\n"):
            numbered_match = re.match(numbered_pattern, line)
            bullet_match = re.match(bullet_pattern, line)

            if numbered_match:
                items.append(numbered_match.group(1).strip())
            elif bullet_match:
                items.append(bullet_match.group(1).strip())

        return items

    @property
    def parsed(self) -> ParsedPRD:
        """Get parsed PRD."""
        if self._parsed is None:
            self.parse()
        assert self._parsed is not None
        return self._parsed

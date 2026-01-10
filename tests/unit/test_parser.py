"""Tests for PRD parser."""

from pathlib import Path

import pytest

from spec_test_generator.parser import PRDParser


class TestPRDParser:
    """Tests for PRDParser class."""

    def test_parse_basic_prd(self, tmp_path: Path) -> None:
        """Test parsing a basic PRD."""
        prd_content = """
# PRD: Test Feature

## Goal
Build something cool

## Functional Requirements
1) First requirement
2) Second requirement

## Non-Goals
- Not doing this
- Not doing that
"""
        prd_file = tmp_path / "prd.md"
        prd_file.write_text(prd_content)

        parser = PRDParser(prd_file)
        result = parser.parse()

        assert result.title == "PRD: Test Feature"
        assert "cool" in result.goal
        assert len(result.functional_requirements) == 2
        assert result.functional_requirements[0] == "First requirement"
        assert len(result.non_goals) == 2

    def test_parse_missing_file(self, tmp_path: Path) -> None:
        """Test parsing a non-existent file."""
        parser = PRDParser(tmp_path / "nonexistent.md")

        with pytest.raises(FileNotFoundError):
            parser.parse()

    def test_parse_bullet_lists(self, tmp_path: Path) -> None:
        """Test parsing bullet-style lists."""
        prd_content = """
# PRD: Test

## Functional Requirements
- First item
- Second item
* Third item
"""
        prd_file = tmp_path / "prd.md"
        prd_file.write_text(prd_content)

        parser = PRDParser(prd_file)
        result = parser.parse()

        assert len(result.functional_requirements) == 3

    def test_parse_notes_section(self, tmp_path: Path) -> None:
        """Test parsing notes section."""
        prd_content = """
# PRD: Test

## Notes
- Important note 1
- Important note 2
"""
        prd_file = tmp_path / "prd.md"
        prd_file.write_text(prd_content)

        parser = PRDParser(prd_file)
        result = parser.parse()

        assert len(result.notes) == 2
        assert "Important note 1" in result.notes[0]

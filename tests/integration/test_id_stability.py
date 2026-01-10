"""Integration tests for ID stability across iterations."""

from pathlib import Path

from spec_test_generator import SpecTestGenerator


class TestIDStability:
    """Tests for ID stability across regenerations."""

    def test_ids_stable_across_runs(self, tmp_path: Path) -> None:
        """Test that IDs remain stable when regenerating."""
        prd_content = """
# PRD: Test Feature

## Goal
Test ID stability

## Functional Requirements
1) Users can log in
2) Users can log out
"""
        prd_file = tmp_path / "prd.md"
        prd_file.write_text(prd_content)
        output_dir = tmp_path / "spec"

        # First run
        generator1 = SpecTestGenerator(prd_file, output_dir=output_dir)
        result1 = generator1.generate()
        req_ids_1 = [r.id for r in result1["requirements"]]

        # Second run
        generator2 = SpecTestGenerator(prd_file, output_dir=output_dir)
        result2 = generator2.generate()
        req_ids_2 = [r.id for r in result2["requirements"]]

        assert req_ids_1 == req_ids_2

    def test_new_requirement_gets_new_id(self, tmp_path: Path) -> None:
        """Test that adding a new requirement gets a new ID."""
        prd_content_v1 = """
# PRD: Test Feature

## Functional Requirements
1) First requirement
"""
        prd_content_v2 = """
# PRD: Test Feature

## Functional Requirements
1) First requirement
2) Second requirement
"""
        prd_file = tmp_path / "prd.md"
        output_dir = tmp_path / "spec"

        # First version
        prd_file.write_text(prd_content_v1)
        generator1 = SpecTestGenerator(prd_file, output_dir=output_dir)
        result1 = generator1.generate()

        # Second version with new requirement
        prd_file.write_text(prd_content_v2)
        generator2 = SpecTestGenerator(prd_file, output_dir=output_dir)
        result2 = generator2.generate()

        assert len(result2["requirements"]) == 2
        # First requirement should keep same ID
        assert result1["requirements"][0].id == result2["requirements"][0].id
        # Second requirement should have new ID
        assert result2["requirements"][1].id == "REQ-0002"

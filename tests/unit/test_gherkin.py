"""Tests for Gherkin generator."""

from pathlib import Path

from spec_test_generator.gherkin import GherkinGenerator
from spec_test_generator.models import Priority, Requirement, TestCase, TestType


class TestGherkinGenerator:
    """Tests for GherkinGenerator class."""

    def test_generate_feature_file(self, tmp_path: Path) -> None:
        """Test generating a feature file from requirements."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="The system SHALL authenticate users",
                    priority=Priority.P0,
                    acceptance_criteria=["Given valid credentials, when login, then success"],
                    edge_cases=["Invalid password"],
                    feature_area="Authentication",
                )
            ],
            "test_cases": [
                TestCase(
                    id="TEST-0001",
                    title="Verify user authentication",
                    test_type=TestType.E2E,
                    priority=Priority.P0,
                    requirement_ids=["REQ-0001"],
                    preconditions="User exists in database",
                    steps=["Enter username", "Enter password", "Click login"],
                    expected=["User is authenticated", "Dashboard is shown"],
                )
            ],
        }

        generator = GherkinGenerator(result, tmp_path)
        artifacts = generator.generate()

        assert len(artifacts) == 1
        feature_path = tmp_path / "features" / "authentication.feature"
        assert feature_path.exists()

        content = feature_path.read_text()
        assert "Feature: Authentication" in content
        assert "Scenario: Verify user authentication" in content
        assert "Given User exists in database" in content

    def test_generate_multiple_features(self, tmp_path: Path) -> None:
        """Test generating multiple feature files."""
        result = {
            "requirements": [
                Requirement(
                    id="REQ-0001",
                    statement="Auth requirement",
                    priority=Priority.P0,
                    acceptance_criteria=["AC1"],
                    feature_area="Auth",
                ),
                Requirement(
                    id="REQ-0002",
                    statement="Payment requirement",
                    priority=Priority.P1,
                    acceptance_criteria=["AC2"],
                    feature_area="Payment",
                ),
            ],
            "test_cases": [],
        }

        generator = GherkinGenerator(result, tmp_path)
        artifacts = generator.generate()

        assert len(artifacts) == 2
        assert (tmp_path / "features" / "auth.feature").exists()
        assert (tmp_path / "features" / "payment.feature").exists()

    def test_sanitize_filename(self, tmp_path: Path) -> None:
        """Test filename sanitization."""
        generator = GherkinGenerator({}, tmp_path)

        assert generator._sanitize_filename("My Feature") == "my_feature"
        assert generator._sanitize_filename("Feature-Name") == "feature_name"
        assert generator._sanitize_filename("A/B Test") == "a_b_test"

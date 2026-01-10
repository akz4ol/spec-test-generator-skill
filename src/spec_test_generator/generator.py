"""Main Spec & Test Generator orchestrator."""

from pathlib import Path
from typing import Any

import yaml

from .id_manager import IDManager
from .models import (
    PolicyConfig,
    Priority,
    Requirement,
    TestCase,
    TestPlan,
    TestType,
    TraceabilityEntry,
)
from .output import OutputGenerator
from .parser import ParsedPRD, PRDParser


class SpecTestGenerator:
    """Main spec and test generation orchestrator."""

    def __init__(
        self,
        prd_path: str | Path,
        policy_path: str | Path | None = None,
        output_dir: str | Path = "spec",
    ):
        """Initialize generator.

        Args:
            prd_path: Path to PRD markdown file
            policy_path: Path to policy YAML file (optional, uses default)
            output_dir: Directory for output artifacts
        """
        self.prd_path = Path(prd_path)
        self.policy_path = Path(policy_path) if policy_path else self._get_default_policy()
        self.output_dir = Path(output_dir)

        self._policy: PolicyConfig | None = None
        self._parser: PRDParser | None = None
        self._id_manager: IDManager | None = None

    def _get_default_policy(self) -> Path:
        """Get path to default policy file."""
        skill_dir = Path(__file__).parent.parent.parent
        return skill_dir / "skills" / "spec-test-generator" / "policy" / "default.internal.yaml"

    def _load_policy(self) -> PolicyConfig:
        """Load policy configuration."""
        if self._policy is not None:
            return self._policy

        if not self.policy_path.exists():
            raise FileNotFoundError(f"Policy file not found: {self.policy_path}")

        with open(self.policy_path) as f:
            data = yaml.safe_load(f)

        self._policy = PolicyConfig.from_dict(data)
        return self._policy

    def _get_id_manager(self) -> IDManager:
        """Get or create ID manager."""
        if self._id_manager is not None:
            return self._id_manager

        policy = self._load_policy()
        self._id_manager = IDManager(
            output_dir=self.output_dir,
            req_prefix=policy.get("ids.requirement_prefix", "REQ"),
            test_prefix=policy.get("ids.test_prefix", "TEST"),
            pad=policy.get("ids.pad", 4),
        )
        return self._id_manager

    def generate(self) -> dict[str, Any]:
        """Generate all spec and test artifacts.

        Returns:
            Dict with requirements, test_plan, test_cases, traceability
        """
        policy = self._load_policy()
        id_manager = self._get_id_manager()

        # Parse PRD
        self._parser = PRDParser(self.prd_path)
        parsed = self._parser.parse()

        # Generate requirements
        requirements = self._generate_requirements(parsed, id_manager, policy)

        # Generate test plan
        test_plan = self._generate_test_plan(parsed, policy)

        # Generate test cases
        test_cases = self._generate_test_cases(requirements, id_manager, policy)

        # Generate traceability
        traceability = self._generate_traceability(test_cases)

        return {
            "requirements": requirements,
            "test_plan": test_plan,
            "test_cases": test_cases,
            "traceability": traceability,
            "open_questions": self._extract_open_questions(parsed),
            "assumptions": parsed.assumptions,
        }

    def _generate_requirements(
        self,
        parsed: ParsedPRD,
        id_manager: IDManager,
        policy: PolicyConfig,
    ) -> list[Requirement]:
        """Generate requirements from parsed PRD."""
        requirements = []
        min_edge_cases = policy.get("requirements.min_edge_cases_per_requirement", 2)

        # Process functional requirements
        for i, req_text in enumerate(parsed.functional_requirements):
            statement_hash = id_manager.hash_statement(req_text)
            req_id = id_manager.get_requirement_id(statement_hash)

            # Determine priority (first few are P0, rest P1)
            priority = Priority.P0 if i < 3 else Priority.P1

            # Generate acceptance criteria from requirement
            acceptance_criteria = self._generate_acceptance_criteria(req_text)

            # Generate edge cases
            edge_cases = self._generate_edge_cases(req_text, min_edge_cases)

            # Normalize statement
            normalized = req_text.lower()
            if normalized.startswith("the system shall "):
                normalized = normalized[17:]
            elif normalized.startswith("shall "):
                normalized = normalized[6:]

            req = Requirement(
                id=req_id,
                statement=f"The system SHALL {normalized}",
                priority=priority,
                acceptance_criteria=acceptance_criteria,
                edge_cases=edge_cases,
                feature_area=parsed.title,
            )
            requirements.append(req)

        # Process non-functional requirements
        for req_text in parsed.non_functional_requirements:
            statement_hash = id_manager.hash_statement(req_text)
            req_id = id_manager.get_requirement_id(statement_hash)

            # Normalize statement
            normalized = req_text.lower()
            if normalized.startswith("the system should "):
                normalized = normalized[18:]
            elif normalized.startswith("should "):
                normalized = normalized[7:]

            req = Requirement(
                id=req_id,
                statement=f"The system SHOULD {normalized}",
                priority=Priority.P1,
                acceptance_criteria=[f"Verify: {req_text}"],
                edge_cases=["Under peak load conditions", "During degraded operations"],
                feature_area="Non-Functional",
            )
            requirements.append(req)

        return requirements

    def _generate_acceptance_criteria(self, req_text: str) -> list[str]:
        """Generate acceptance criteria from requirement text."""
        criteria = []

        # Basic happy path
        criteria.append(
            f"Given valid input, when the operation is performed, then {req_text.lower()}"
        )

        # Error handling
        if any(word in req_text.lower() for word in ["must", "required", "authenticated"]):
            criteria.append(
                "Given invalid input, when the operation is attempted, then the system returns an appropriate error"
            )

        return criteria

    def _generate_edge_cases(self, req_text: str, min_count: int) -> list[str]:
        """Generate edge cases from requirement text."""
        edge_cases = []

        # Common edge cases based on keywords
        if "list" in req_text.lower() or "pagination" in req_text.lower():
            edge_cases.extend(
                [
                    "Empty result set",
                    "Single item result",
                    "Maximum page size exceeded",
                ]
            )

        if "auth" in req_text.lower():
            edge_cases.extend(
                [
                    "Expired credentials",
                    "Missing credentials",
                    "Invalid token format",
                ]
            )

        if "error" in req_text.lower():
            edge_cases.extend(
                [
                    "Network timeout",
                    "Malformed request",
                ]
            )

        # Ensure minimum edge cases
        generic_cases = [
            "Invalid input format",
            "Boundary value conditions",
            "Concurrent access scenario",
            "System under load",
        ]

        while len(edge_cases) < min_count:
            for gc in generic_cases:
                if gc not in edge_cases:
                    edge_cases.append(gc)
                    break
            else:
                break

        return edge_cases[: min_count + 2]  # Slightly over minimum

    def _generate_test_plan(self, parsed: ParsedPRD, policy: PolicyConfig) -> TestPlan:
        """Generate test plan from parsed PRD."""
        strategy = {}

        if policy.get("tests.types.unit", True):
            strategy["Unit tests"] = "Request validation, business logic, formatting"

        if policy.get("tests.types.integration", True):
            strategy["Integration tests"] = (
                "Database operations, external service calls, auth middleware"
            )

        if policy.get("tests.types.e2e", True):
            rule = policy.get("tests.e2e_selection_rule", "only_top_flows")
            if rule == "only_top_flows":
                strategy["E2E tests"] = "Top user flows only (happy path + critical errors)"
            else:
                strategy["E2E tests"] = "All P0 flows and critical paths"

        test_data = [
            "Seed representative dataset for integration tests",
            "Include edge case data (empty values, boundary conditions)",
        ]

        environments = {
            "CI": "Unit + lightweight integration tests",
            "Staging": "Full integration + E2E tests",
        }

        non_functional = []
        if parsed.non_functional_requirements:
            non_functional.append("Performance smoke tests")
        if any("auth" in r.lower() for r in parsed.functional_requirements):
            non_functional.append("Security tests for authentication flows")

        return TestPlan(
            strategy=strategy,
            test_data=test_data,
            environments=environments,
            non_functional=non_functional,
        )

    def _generate_test_cases(
        self,
        requirements: list[Requirement],
        id_manager: IDManager,
        policy: PolicyConfig,
    ) -> list[TestCase]:
        """Generate test cases from requirements."""
        test_cases = []
        _min_tests = policy.get("tests.require_min_tests_per_requirement", 1)  # noqa: F841
        include_negative = policy.get("tests.include_negative_tests", True)

        for req in requirements:
            # Happy path test
            test_hash = id_manager.hash_test(f"Happy path for {req.id}", [req.id])
            test_id = id_manager.get_test_id(test_hash)

            # Determine test type based on requirement
            test_type = TestType.UNIT
            if "integration" in req.statement.lower() or "database" in req.statement.lower():
                test_type = TestType.INTEGRATION
            elif req.priority == Priority.P0 and "user" in req.statement.lower():
                test_type = TestType.E2E

            test = TestCase(
                id=test_id,
                title=f"Verify {req.statement[:50]}...",
                test_type=test_type,
                priority=req.priority,
                requirement_ids=[req.id],
                preconditions="Valid test environment setup",
                steps=["Set up test preconditions", "Execute the operation", "Verify results"],
                expected=["Operation succeeds", "Results match expected values"],
            )
            test_cases.append(test)

            # Negative test if required
            if include_negative and req.edge_cases:
                neg_hash = id_manager.hash_test(f"Negative test for {req.id}", [req.id])
                neg_id = id_manager.get_test_id(neg_hash)

                neg_test = TestCase(
                    id=neg_id,
                    title=f"Negative: {req.edge_cases[0]}",
                    test_type=TestType.UNIT,
                    priority=req.priority,
                    requirement_ids=[req.id],
                    preconditions="None or invalid state",
                    steps=["Attempt operation with invalid input"],
                    expected=["Appropriate error returned", "No side effects"],
                )
                test_cases.append(neg_test)

        return test_cases

    def _generate_traceability(self, test_cases: list[TestCase]) -> list[TraceabilityEntry]:
        """Generate traceability entries from test cases."""
        entries = []

        for test in test_cases:
            for req_id in test.requirement_ids:
                entries.append(
                    TraceabilityEntry(
                        req_id=req_id,
                        test_id=test.id,
                        test_type=test.test_type,
                        priority=test.priority,
                    )
                )

        return entries

    def _extract_open_questions(self, parsed: ParsedPRD) -> list[str]:
        """Extract open questions from PRD."""
        questions = []

        # Look for question marks in notes
        for note in parsed.notes:
            if "?" in note:
                questions.append(note)

        # Add generic questions for common ambiguities
        if any("auth" in r.lower() for r in parsed.functional_requirements):
            questions.append("What is the authentication provider/mechanism?")

        return questions

    def write_artifacts(self, result: dict[str, Any] | None = None) -> dict[str, Path]:
        """Write all artifacts to output directory.

        Args:
            result: Generation result (runs generate() if not provided)

        Returns:
            Dict mapping artifact names to file paths
        """
        if result is None:
            result = self.generate()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        policy = self._load_policy()

        generator = OutputGenerator(result, policy, self.output_dir)
        return generator.generate_all()

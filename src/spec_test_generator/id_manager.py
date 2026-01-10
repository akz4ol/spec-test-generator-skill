"""Stable ID management for requirements and tests."""

import json
from pathlib import Path
from typing import Any, cast


class IDManager:
    """Manages stable IDs for requirements and tests."""

    def __init__(
        self,
        output_dir: Path,
        req_prefix: str = "REQ",
        test_prefix: str = "TEST",
        pad: int = 4,
    ):
        """Initialize ID manager.

        Args:
            output_dir: Directory for .idmap.json persistence
            req_prefix: Prefix for requirement IDs
            test_prefix: Prefix for test IDs
            pad: Zero-padding width for ID numbers
        """
        self.output_dir = output_dir
        self.req_prefix = req_prefix
        self.test_prefix = test_prefix
        self.pad = pad

        self._idmap_path = output_dir / ".idmap.json"
        self._idmap: dict[str, Any] = self._load_idmap()

        self._next_req_num = self._get_next_number("requirements")
        self._next_test_num = self._get_next_number("tests")

    def _load_idmap(self) -> dict[str, Any]:
        """Load existing ID map if present."""
        if self._idmap_path.exists():
            try:
                with open(self._idmap_path) as f:
                    return cast(dict[str, Any], json.load(f))
            except (OSError, json.JSONDecodeError):
                pass
        return {
            "requirements": {},
            "tests": {},
            "metadata": {
                "version": "1.0",
                "req_prefix": self.req_prefix,
                "test_prefix": self.test_prefix,
            },
        }

    def _save_idmap(self) -> None:
        """Save ID map to disk."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self._idmap_path, "w") as f:
            json.dump(self._idmap, f, indent=2)

    def _get_next_number(self, category: str) -> int:
        """Get next available number for a category."""
        existing = self._idmap.get(category, {})
        if not existing:
            return 1

        # Extract numbers from existing IDs
        numbers = []
        for id_str in existing.values():
            try:
                num = int(id_str.split("-")[1])
                numbers.append(num)
            except (IndexError, ValueError):
                pass

        return max(numbers, default=0) + 1

    def get_requirement_id(self, statement_hash: str) -> str:
        """Get or create a requirement ID for a statement.

        Args:
            statement_hash: Hash or fingerprint of the requirement statement

        Returns:
            Stable requirement ID (e.g., REQ-0001)
        """
        requirements = self._idmap.setdefault("requirements", {})

        if statement_hash in requirements:
            return cast(str, requirements[statement_hash])

        # Allocate new ID
        new_id = f"{self.req_prefix}-{str(self._next_req_num).zfill(self.pad)}"
        requirements[statement_hash] = new_id
        self._next_req_num += 1
        self._save_idmap()

        return new_id

    def get_test_id(self, test_hash: str) -> str:
        """Get or create a test ID for a test case.

        Args:
            test_hash: Hash or fingerprint of the test case

        Returns:
            Stable test ID (e.g., TEST-0001)
        """
        tests = self._idmap.setdefault("tests", {})

        if test_hash in tests:
            return cast(str, tests[test_hash])

        # Allocate new ID
        new_id = f"{self.test_prefix}-{str(self._next_test_num).zfill(self.pad)}"
        tests[test_hash] = new_id
        self._next_test_num += 1
        self._save_idmap()

        return new_id

    def get_all_requirement_ids(self) -> list[str]:
        """Get all allocated requirement IDs."""
        return list(self._idmap.get("requirements", {}).values())

    def get_all_test_ids(self) -> list[str]:
        """Get all allocated test IDs."""
        return list(self._idmap.get("tests", {}).values())

    @staticmethod
    def hash_statement(statement: str) -> str:
        """Create a hash/fingerprint for a statement.

        Uses first N significant words to allow minor edits without ID change.
        """
        import hashlib

        # Normalize: lowercase, remove extra whitespace
        normalized = " ".join(statement.lower().split())

        # Strip trailing punctuation before fingerprinting
        normalized = normalized.rstrip(".,!?;:")

        # Take first ~50 chars for fingerprint stability
        fingerprint = normalized[:50]

        return hashlib.md5(fingerprint.encode()).hexdigest()[:12]

    @staticmethod
    def hash_test(title: str, req_ids: list[str]) -> str:
        """Create a hash/fingerprint for a test case."""
        import hashlib

        # Combine title and requirements for uniqueness
        combined = f"{title.lower()}:{','.join(sorted(req_ids))}"

        return hashlib.md5(combined.encode()).hexdigest()[:12]

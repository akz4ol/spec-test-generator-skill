"""Tests for ID manager."""

import pytest
from pathlib import Path

from spec_test_generator.id_manager import IDManager


class TestIDManager:
    """Tests for IDManager class."""

    def test_allocate_requirement_id(self, tmp_path: Path) -> None:
        """Test allocating a new requirement ID."""
        manager = IDManager(tmp_path)

        id1 = manager.get_requirement_id("hash1")
        id2 = manager.get_requirement_id("hash2")

        assert id1 == "REQ-0001"
        assert id2 == "REQ-0002"

    def test_stable_requirement_id(self, tmp_path: Path) -> None:
        """Test that same hash returns same ID."""
        manager = IDManager(tmp_path)

        id1 = manager.get_requirement_id("hash1")
        id2 = manager.get_requirement_id("hash1")

        assert id1 == id2 == "REQ-0001"

    def test_allocate_test_id(self, tmp_path: Path) -> None:
        """Test allocating a new test ID."""
        manager = IDManager(tmp_path)

        id1 = manager.get_test_id("testhash1")
        id2 = manager.get_test_id("testhash2")

        assert id1 == "TEST-0001"
        assert id2 == "TEST-0002"

    def test_persistence(self, tmp_path: Path) -> None:
        """Test that IDs persist across manager instances."""
        # First manager
        manager1 = IDManager(tmp_path)
        id1 = manager1.get_requirement_id("persistent_hash")
        assert id1 == "REQ-0001"

        # Second manager instance
        manager2 = IDManager(tmp_path)
        id2 = manager2.get_requirement_id("persistent_hash")
        assert id2 == "REQ-0001"  # Should be same

        # New hash should get next ID
        id3 = manager2.get_requirement_id("new_hash")
        assert id3 == "REQ-0002"

    def test_custom_prefix(self, tmp_path: Path) -> None:
        """Test custom ID prefixes."""
        manager = IDManager(
            tmp_path,
            req_prefix="SPEC",
            test_prefix="TC",
        )

        req_id = manager.get_requirement_id("hash")
        test_id = manager.get_test_id("testhash")

        assert req_id == "SPEC-0001"
        assert test_id == "TC-0001"

    def test_hash_statement(self) -> None:
        """Test statement hashing."""
        hash1 = IDManager.hash_statement("The system shall do something")
        hash2 = IDManager.hash_statement("The system shall do something")
        hash3 = IDManager.hash_statement("The system shall do something else")

        assert hash1 == hash2
        assert hash1 != hash3

    def test_hash_statement_minor_changes(self) -> None:
        """Test that minor changes to statement still match."""
        hash1 = IDManager.hash_statement("The system shall authenticate users")
        hash2 = IDManager.hash_statement("The system shall authenticate users.")

        # First 50 chars should be same, so hashes match
        assert hash1 == hash2

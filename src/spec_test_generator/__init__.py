"""Spec & Test Generator - Convert PRDs to requirements and test artifacts."""

__version__ = "1.0.0"

from .generator import SpecTestGenerator
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
from .parser import PRDParser

__all__ = [
    "SpecTestGenerator",
    "Requirement",
    "TestCase",
    "TestPlan",
    "TraceabilityEntry",
    "PolicyConfig",
    "Priority",
    "TestType",
    "PRDParser",
    "IDManager",
]

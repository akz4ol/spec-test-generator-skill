"""Spec & Test Generator - Convert PRDs to requirements and test artifacts."""

__version__ = "1.0.0"

from .generator import SpecTestGenerator
from .models import (
    Requirement,
    TestCase,
    TestPlan,
    TraceabilityEntry,
    PolicyConfig,
    Priority,
    TestType,
)
from .parser import PRDParser
from .id_manager import IDManager

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

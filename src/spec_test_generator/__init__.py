"""Spec & Test Generator - Convert PRDs to requirements and test artifacts."""

__version__ = "1.0.0"

from .coverage import CoverageAnalyzer, CoverageReport
from .generator import SpecTestGenerator
from .gherkin import GherkinGenerator
from .id_manager import IDManager
from .impact import ImpactAnalyzer, ImpactReport
from .importers import JiraImporter, LinearImporter
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
    "GherkinGenerator",
    "JiraImporter",
    "LinearImporter",
    "CoverageAnalyzer",
    "CoverageReport",
    "ImpactAnalyzer",
    "ImpactReport",
]

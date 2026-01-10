# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation

## [1.0.0] - 2025-01-10

### Added
- Core spec & test generator skill with SKILL.md definition
- Pragmatic internal policy (`default.internal.yaml`)
  - REQ-xxxx stable requirement IDs
  - TEST-xxxx stable test case IDs
  - Given-When-Then or bullet acceptance criteria
  - Minimum 1 test per requirement
  - Security tests when auth present
- Strict regulated policy (`preset.strict.yaml`)
  - Minimum 2 tests per requirement
  - Minimum 1 negative test per requirement
  - Required rationale and out-of-scope fields
  - Bidirectional traceability notes
- Stable ID management
  - IDs preserved across iterations
  - Smart ID allocation on requirement splits
  - `.idmap.json` for ID persistence
- Output artifact generation
  - `REQUIREMENTS.md` with structured requirements
  - `TEST_PLAN.md` with test pyramid strategy
  - `TEST_CASES.md` with detailed test cases
  - `TRACEABILITY.csv` with REQ-TEST mapping
- CLI tool (`spec-test-generator`)
- Python API for programmatic use
- JSON schema for policy validation
- Example PRD input and expected outputs
- GitHub Actions CI/CD pipeline
- Docker support for containerized execution

### Documentation
- Comprehensive SKILL.md with procedure steps
- README with quick start guide
- CONTRIBUTING.md with development guidelines
- API documentation in `docs/`

## [0.1.0] - 2025-01-10

### Added
- Initial project structure
- Basic skill definition

[Unreleased]: https://github.com/yourorg/spec-test-generator-skill/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourorg/spec-test-generator-skill/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/yourorg/spec-test-generator-skill/releases/tag/v0.1.0

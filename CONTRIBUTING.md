# Contributing to Spec & Test Generator Skill

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Policy Contributions](#policy-contributions)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project follows a standard code of conduct. Be respectful, inclusive, and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Make (optional, for convenience commands)

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/spec-test-generator-skill.git
cd spec-test-generator-skill
```

## Development Setup

### Using Make (Recommended)

```bash
make install      # Install dependencies
make test         # Run tests
make lint         # Run linters
make format       # Format code
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Verify installation
python -m spec_test_generator --help
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(ids): add support for custom ID prefixes
fix(traceability): correct bidirectional mapping generation
docs(readme): add policy customization examples
```

## Policy Contributions

### Adding a New Policy Preset

1. Create the policy file in `skills/spec-test-generator/policy/`
2. Follow the schema in `schemas/policy.schema.json`
3. Add example PRD that demonstrates the policy
4. Document the policy use case in the README

### Policy File Structure

```yaml
policy_name: "Your Policy Name"
policy_version: "1.0"

ids:
  requirement_prefix: "REQ"
  test_prefix: "TEST"
  # ...

requirements:
  # Requirement rules...

tests:
  # Test generation rules...

traceability:
  # Traceability rules...
```

### Validation

```bash
# Validate policy against schema
make validate-policy POLICY=policy/your-policy.yaml
```

## Testing

### Running Tests

```bash
# All tests
make test

# Specific test file
pytest tests/test_id_stability.py

# With coverage
make coverage
```

### Test Structure

```
tests/
├── unit/
│   ├── test_parser.py
│   ├── test_id_manager.py
│   └── test_generators.py
├── integration/
│   ├── test_full_generation.py
│   └── test_iterative_updates.py
└── fixtures/
    ├── prds/
    └── policies/
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use fixtures from `tests/fixtures/` or create new ones
- Aim for >80% code coverage on new code
- Test ID stability across iterations

## Pull Request Process

### Before Submitting

1. Ensure all tests pass: `make test`
2. Run linters: `make lint`
3. Format code: `make format`
4. Update documentation if needed
5. Add/update tests for your changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] ID stability tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### Review Process

1. Submit PR against `main` branch
2. Automated CI checks must pass
3. At least one maintainer approval required
4. Squash and merge preferred

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes to artifact format or policy schema
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Release Checklist

1. Update `CHANGELOG.md`
2. Update version in `pyproject.toml`
3. Create release PR
4. After merge, tag the release
5. GitHub Actions publishes automatically

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas

Thank you for contributing!

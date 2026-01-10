# Cross-Repo Outreach Strategy

Adjacent repos to integrate with or link from.

---

## High Priority (Direct Overlap)

### 1. pytest-bdd (pytest-dev/pytest-bdd)
**Stars**: 1.3k+ | **Relationship**: Output format target

**Action**: Open discussion about Gherkin export
```
Title: Generate Gherkin scenarios from PRDs

Working on spec-test-generator which converts PRDs to requirements and test cases.

Considering adding Gherkin/BDD output format for pytest-bdd compatibility.

Would love feedback on format preferences from pytest-bdd users.
```

### 2. behave (behave/behave)
**Stars**: 3k+ | **Relationship**: Output format target

**Action**: Community discussion
```
Title: PRD → Feature Files automation

spec-test-generator can convert PRDs to requirements and test cases.
Exploring Gherkin output for behave integration.
```

### 3. allure-pytest (allure-framework/allure-python)
**Stars**: 700+ | **Relationship**: Test reporting integration

**Action**: Propose linking test IDs to Allure
```
Title: Stable test case IDs for Allure integration

spec-test-generator assigns stable IDs (TEST-0001) using content fingerprints.

Could these IDs integrate with Allure for cross-run tracking?
```

---

## Medium Priority (Requirements Management)

### 4. doorstop (doorstop-dev/doorstop)
**Stars**: 400+ | **Relationship**: Direct overlap

**Action**: Add to related projects or compare
```
Title: doorstop vs spec-test-generator comparison

doorstop: Full requirements management system
spec-test-generator: PRD → specs snapshot generator

Different use cases:
- doorstop for ongoing requirements lifecycle
- spec-test-generator for quick PRD conversion with stable IDs
```

### 5. sphinx-needs (useblacksmith/sphinx-needs)
**Stars**: 200+ | **Relationship**: Documentation integration

**Action**: Propose export format
```
Title: Export to sphinx-needs format

spec-test-generator could export requirements in sphinx-needs format
for integration with Sphinx documentation.
```

---

## Medium Priority (Test Management)

### 6. pytest (pytest-dev/pytest)
**Stars**: 11k+ | **Relationship**: User overlap

**Action**: Community discussion about markers
```
Title: Generating pytest markers from requirement IDs

spec-test-generator assigns stable IDs like TEST-0001.

Workflow idea:
1. Generate test cases from PRD
2. Add pytest markers: @pytest.mark.req("REQ-0001")
3. Track coverage via markers
```

### 7. robot-framework (robotframework/robotframework)
**Stars**: 9k+ | **Relationship**: Output format target

**Action**: Explore Robot Framework export
```
Title: PRD → Robot Framework test cases

Exploring export formats for spec-test-generator.
Would Robot Framework syntax be useful?
```

---

## Lower Priority (Broader Ecosystem)

### 8. pydantic (pydantic/pydantic)
**Stars**: 18k+ | **Relationship**: Model validation inspiration

**Action**: Community mention
```
Pattern: PRD → Requirements (pydantic models) → Test Cases
Validate requirement structure with pydantic.
```

### 9. jira-python (pycontribs/jira)
**Stars**: 1.8k+ | **Relationship**: Potential import source

**Action**: Feature discussion
```
Title: Import from Jira epics/stories

Could spec-test-generator import from Jira as an alternative to PRD markdown?
```

### 10. testrail-api (tolstislon/testrail-api)
**Stars**: 100+ | **Relationship**: Export target

**Action**: Export format proposal
```
Title: TestRail export format

For teams using TestRail, could export test cases in TestRail import format.
```

---

## Outreach Templates

### PR Template: Add to Related Projects

```markdown
## Description
Add spec-test-generator to the list of related projects.

spec-test-generator provides:
- PRD → structured requirements with stable IDs
- Test case generation with fingerprint-based IDs
- Traceability matrix generation

## Why Related
[Explain how it complements this project]

## Links
- GitHub: https://github.com/akz4ol/spec-test-generator-skill
- Docs: https://akz4ol.github.io/spec-test-generator-skill
```

### Issue Template: Propose Output Format

```markdown
## Summary
Proposing [format] export for spec-test-generator.

## What spec-test-generator Does
- Converts PRDs to requirements (REQ-xxxx) and test cases (TEST-xxxx)
- Uses content fingerprints for stable IDs
- Generates traceability matrices

## Proposed Format
[Describe the export format]

## Use Case
[Who would use this and why]

## Questions
1. What format details matter for [target project]?
2. Any specific conventions to follow?
```

---

## Tracking

| Repo | Action | Status | Date | Response |
|------|--------|--------|------|----------|
| pytest-bdd | Discussion | TODO | | |
| behave | Discussion | TODO | | |
| allure-pytest | Issue | TODO | | |
| doorstop | Compare | TODO | | |
| sphinx-needs | Discussion | TODO | | |
| pytest | Discussion | TODO | | |
| robot-framework | Discussion | TODO | | |

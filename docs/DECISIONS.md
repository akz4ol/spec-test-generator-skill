# Architectural Decision Records

This document captures key architectural decisions made in spec-test-generator.

---

## ADR-001: Fingerprint-Based Stable IDs

**Date**: 2024-01

### Context

Requirements and test cases need stable identifiers that survive regeneration. Sequential numbering breaks when content changes.

### Options Considered

1. **Sequential IDs** — Simple but unstable (REQ-0001 becomes REQ-0002 after insertion)
2. **UUID** — Stable but not human-readable or memorable
3. **Content fingerprint** — Stable and reasonably human-friendly

### Decision

Use content fingerprint (hash of normalized text) to generate stable IDs. Map fingerprint → ID in `.idmap.json`.

### Consequences

- **Positive**: IDs survive minor edits (whitespace, typos)
- **Positive**: Human-readable format (REQ-0001)
- **Negative**: Requires persisting `.idmap.json`
- **Mitigated by**: Clear guidance to commit .idmap.json

---

## ADR-002: Separate ID Namespaces for Requirements and Tests

**Date**: 2024-01

### Context

Need to distinguish requirements from test cases in references.

### Decision

Use separate namespaces:
- Requirements: REQ-0001, REQ-0002, ...
- Test Cases: TEST-0001, TEST-0002, ...

### Consequences

- **Positive**: Unambiguous references in bug reports, conversations
- **Positive**: Can search codebase for "REQ-0042" vs "TEST-0042"
- **Negative**: Slightly longer identifiers
- **Acceptable**: Industry standard practice

---

## ADR-003: Traceability as CSV (Not Embedded)

**Date**: 2024-01

### Context

Need bidirectional mapping between requirements and test cases.

### Options Considered

1. **Embed in markdown** — Single file but hard to parse programmatically
2. **JSON** — Machine-readable but not spreadsheet-friendly
3. **CSV** — Machine-readable AND opens in Excel/Sheets

### Decision

Generate `TRACEABILITY.csv` with columns: REQ_ID, TEST_ID, Requirement Summary, Test Summary.

### Consequences

- **Positive**: Opens directly in spreadsheets for auditors
- **Positive**: Easy to grep/filter programmatically
- **Negative**: Another file to track
- **Mitigated by**: Auto-generated, not hand-maintained

---

## ADR-004: .idmap.json as Source of Truth

**Date**: 2024-01

### Context

ID stability requires persistence across regenerations.

### Decision

Store fingerprint-to-ID mappings in `.idmap.json` alongside outputs.

```json
{
  "requirements": {"fingerprint": "REQ-0001"},
  "tests": {"fingerprint": "TEST-0001"},
  "next_req_id": 2,
  "next_test_id": 2
}
```

### Consequences

- **Positive**: IDs persist across machines when committed
- **Positive**: Human-readable JSON for debugging
- **Negative**: File can get large with many requirements
- **Mitigated by**: Fingerprints are small strings, file stays manageable

---

## ADR-005: Policy-Driven Strictness Levels

**Date**: 2024-01

### Context

Different contexts need different rigor (startup vs. regulated industry).

### Options Considered

1. **Single behavior** — Simple but inflexible
2. **Flags (--strict)** — Quick but limited
3. **Policy files** — Full configurability

### Decision

Use YAML policy files with presets: `default.internal.yaml` (pragmatic) and `preset.strict.yaml` (regulated).

### Consequences

- **Positive**: One tool for all contexts
- **Positive**: Presets enable quick start
- **Negative**: Another configuration format to learn
- **Mitigated by**: Sensible defaults, clear examples

---

## ADR-006: Never Reuse Retired IDs

**Date**: 2024-01

### Context

When a requirement is deleted, its ID could be reused for new content.

### Decision

Never reuse IDs. Once REQ-0042 is allocated, it's never used again even if the requirement is deleted.

### Consequences

- **Positive**: Historical references remain valid (bug reports, test runs)
- **Positive**: No confusion about "which REQ-0042"
- **Negative**: IDs may have gaps (REQ-0001, REQ-0003 if REQ-0002 deleted)
- **Acceptable**: Gaps don't affect functionality

---

## ADR-007: Markdown for Human-Readable Output

**Date**: 2024-01

### Context

Output needs to be readable by humans and trackable in git.

### Decision

Generate markdown files: REQUIREMENTS.md, TEST_PLAN.md, TEST_CASES.md.

### Consequences

- **Positive**: Renders nicely on GitHub/GitLab
- **Positive**: Diff-able in PRs
- **Positive**: Can be printed/exported as needed
- **Negative**: Not directly importable to Jira/TestRail
- **Future**: Add export formats (Gherkin, XML)

---

## ADR-008: PRD Parsing is Best-Effort

**Date**: 2024-01

### Context

PRDs come in many formats. Can't mandate strict structure.

### Decision

Parser is best-effort with fallbacks:
- Look for standard headers (Goal, Requirements, Non-Goals)
- Fall back to bullet extraction if headers missing
- Warn but continue on unrecognized structure

### Consequences

- **Positive**: Works with many PRD styles
- **Negative**: May miss requirements in unusual formats
- **Mitigated by**: Clear input format guidance in docs

---

## Future Decisions to Make

- [ ] Gherkin/BDD output format
- [ ] Import from Jira/Linear
- [ ] Delta reports (what changed since last generation)
- [ ] Team collaboration (multiple .idmap.json merge strategy)

# Launch Kit: spec-test-generator

Launch assets for distributing spec-test-generator to developer communities.

---

## Twitter/X Threads

### Thread 1: Problem-First

```
1/ "Which REQ-0042 are we talking about?"

Every PRD iteration breaks requirement IDs.
Bug reports reference invalid numbers.
Traceability is a lie.

We fixed this with content-fingerprinted IDs. Thread 👇

2/ The problem with sequential IDs:

PRD v1: REQ-0001, REQ-0002, REQ-0003
PRD v2: *adds requirement*
PRD v2: REQ-0001, REQ-0002, REQ-0003, REQ-0004

But wait - REQ-0002 in v2 isn't the same as REQ-0002 in v1.
All your bug reports just became invalid.

3/ Our solution: fingerprint-based IDs.

We hash the requirement content.
Same content → same fingerprint → same ID.

Edit a typo? ID stays the same.
Reorder requirements? IDs stay the same.

4/ How it works:

$ spec-test-generator prd.md

Creates:
- REQUIREMENTS.md (REQ-0001, REQ-0002, ...)
- TEST_CASES.md (TEST-0001, TEST-0002, ...)
- TRACEABILITY.csv (which tests cover which reqs)
- .idmap.json (the magic persistence file)

5/ The .idmap.json file stores fingerprint → ID mappings.

Commit it to git.
Now everyone on your team gets the same IDs.
Regenerate anytime—IDs persist.

6/ Bonus: we generate traceability matrices automatically.

REQ-0001 → TEST-0001, TEST-0002
REQ-0002 → TEST-0003

Auditors love this. Compliance teams love this.

7/ Try it:

pip install spec-test-generator
spec-test-generator your-prd.md

GitHub: github.com/akz4ol/spec-test-generator-skill

MIT licensed.
```

### Thread 2: Traceability Focus

```
1/ "How do I know which tests cover this requirement?"

If you're managing traceability in spreadsheets, this thread is for you. 🧵

2/ Manual traceability problems:

- Spreadsheets get out of sync
- No one updates after code changes
- Audits become archaeology projects
- "We have tests somewhere for this..."

3/ Automated traceability:

spec-test-generator reads your PRD and generates:
- Requirements with stable IDs
- Test cases linked to requirements
- CSV traceability matrix

All from a single source of truth.

4/ The TRACEABILITY.csv:

REQ_ID,TEST_ID,Requirement,Test
REQ-0001,TEST-0001,User can login,Verify login with valid credentials
REQ-0001,TEST-0002,User can login,Verify login fails with wrong password

Opens directly in Excel for auditors.

5/ The magic: regenerate anytime.

Edit your PRD. Run spec-test-generator again.
Traceability updates automatically.
IDs stay stable (fingerprint-based).

github.com/akz4ol/spec-test-generator-skill
```

### Thread 3: Compliance Focus

```
1/ Shipping software to regulated industries? (fintech, healthcare, defense)

You need traceable requirements and test cases.

Here's how we automate this. 👇

2/ Compliance audits ask:

"Show me the requirement for this feature."
"Show me the tests that cover this requirement."
"Prove nothing is untested."

3/ spec-test-generator generates audit-ready artifacts:

REQUIREMENTS.md - structured requirements with stable IDs
TEST_PLAN.md - test pyramid strategy
TEST_CASES.md - detailed test cases
TRACEABILITY.csv - bidirectional coverage matrix

4/ Strict mode for regulated environments:

$ spec-test-generator prd.md --strict

Requires:
- 2+ tests per requirement
- Negative test cases
- Full traceability (no gaps)
- GWT acceptance criteria format

5/ Everything regenerates from the PRD.

Update requirements? Run again.
Artifacts stay in sync.
Audit trail in git history.

github.com/akz4ol/spec-test-generator-skill
```

---

## Hacker News Post

### Ask HN: How do you maintain requirement-to-test traceability?

```
Working on a compliance-heavy project and struggling to keep requirement IDs stable across PRD iterations.

Every time we update the PRD, the sequential numbering shifts, which breaks references in:
- Bug reports
- Test run results
- Design documents
- Sprint tickets

We built a tool that uses content fingerprints instead of sequential numbers. Same requirement content = same ID, even after regeneration.

It also generates traceability matrices automatically (which tests cover which requirements).

GitHub: https://github.com/akz4ol/spec-test-generator-skill

How do others handle this? Manual spreadsheets? Jira linking? Something else?
```

---

## Reddit Posts

### r/programming

**Title:** Stable requirement IDs that survive PRD changes - fingerprint-based approach

```
We got tired of "which REQ-0042 are we talking about?" conversations after every PRD update.

Built a tool that assigns IDs based on content fingerprints instead of sequential numbers:

- Edit a typo → same ID
- Reorder sections → same ID
- Major rewrite → new ID (correctly)

Also generates test cases and traceability matrices.

The .idmap.json file persists the fingerprint→ID mappings. Commit it to git, and everyone gets consistent IDs.

GitHub: https://github.com/akz4ol/spec-test-generator-skill

MIT licensed, Python 3.10+.
```

### r/QualityAssurance

**Title:** Automating requirements-to-test traceability from PRDs

```
For QA folks dealing with traceability matrices:

spec-test-generator takes a PRD (markdown) and outputs:
- REQUIREMENTS.md with stable IDs
- TEST_CASES.md with test cases per requirement
- TRACEABILITY.csv for auditors

The IDs are fingerprint-based, so they don't change when you regenerate.

Works well for:
- Compliance audits (fintech, healthcare)
- Sprint planning (break epics into testable chunks)
- Coverage analysis (what's untested?)

https://github.com/akz4ol/spec-test-generator-skill

Would love feedback from QA folks on what output formats would be useful (Gherkin? TestRail import?).
```

---

## GitHub Discussions Seeds

### Discussion 1: Output Format Requests

**Title:** What output formats would you use?

```
Currently we generate:
- Markdown (REQUIREMENTS.md, TEST_CASES.md)
- CSV (TRACEABILITY.csv)

What other formats would be useful?

Considering:
- Gherkin/BDD format
- XML (xUnit style)
- JSON
- Jira import format
- TestRail import format

What would help your workflow most?
```

### Discussion 2: PRD Format Examples

**Title:** Share your PRD formats

```
spec-test-generator parses markdown PRDs with sections like:
- Goal
- Functional Requirements
- Non-Functional Requirements
- Non-Goals

What does your team's PRD format look like?

We want to improve parsing for different styles. Share examples and we'll try to support them!
```

### Discussion 3: ID Stability Stories

**Title:** Has stable IDs helped your workflow?

```
We'd love to hear stories about how fingerprint-based IDs have (or haven't) helped.

Questions:
- How often do you regenerate specs?
- Have stable IDs improved bug report references?
- Any edge cases where IDs changed unexpectedly?

Share your experience!
```

---

## Adjacent Repo Outreach

See [OUTREACH.md](OUTREACH.md) for the cross-repo integration strategy.

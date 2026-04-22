# Workflow: Match

Triggered by: "match [candidate] to [job]"

## Steps

1. **Load** the candidate page from `candidates/`
2. **Load** the job page from `jobs/`
3. **Compare** each requirement against the candidate's skills and experience
4. **Classify** each criterion using three states:
   - ✅ **Matched** — explicitly evidenced in candidate page
   - ⚠️ **Gap** — required but not evidenced
   - 🔵 **Hidden** — likely present but not on CV; flag for discussion
5. **Produce** a match table (see template below)
6. **Write** narrative summary — lead with strengths, name gaps honestly, surface hidden skills
7. **File** to `synthesis/Match Analysis — [Candidate] vs [Job].md`
8. **Link** the synthesis page from both the candidate and job pages
9. **Append** entry to `log.md`

## Match Table Template

| Requirement | Status | Evidence |
|-------------|--------|----------|
| [Skill/requirement] | ✅/⚠️/🔵 | [Source or note] |

## Narrative Template

```markdown
## Strengths
[What the candidate demonstrably brings]

## Gaps
[What's missing — be specific, not vague]

## Hidden Skills
[What likely exists but isn't evidenced — flag for interview or portfolio]

## Verdict
[One paragraph: fit, risk, recommendation]
```

## Rules
- Never round up ⚠️ gaps to ✅ matches — honesty compounds over time
- Always surface 🔵 hidden skills — these are conversation starters
- One synthesis page per candidate-job pair
- Link synthesis from both source pages

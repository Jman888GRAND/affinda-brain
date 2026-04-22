# Workflow: Query

Triggered by: any question about the graph

## Steps

1. **Identify** what kind of query it is (see types below)
2. **Load** only the pages required — never speculative reads
3. **Synthesise** an answer from compiled wiki pages (not raw JSON)
4. **Respond** with a direct answer
5. **File** to `synthesis/` if the answer is reusable or non-trivial (see rule below)
6. **Append** to `log.md` if the query produced a new synthesis page

## Query Types

| Type | Example | Pages to Load |
|------|---------|---------------|
| Candidate lookup | "What does James know?" | `candidates/[Name].md` |
| Skill lookup | "Who has Python?" | `skills/Python.md` |
| Org lookup | "What's Monash?" | `organisations/Monash University.md` |
| Match | "How does James fit the Affinda role?" | → trigger `workflow/match.md` |
| Gap analysis | "What skills is James missing?" | Candidate + Job pages |
| Cross-graph | "What skills appear in multiple candidates?" | Relevant `skills/` pages |

## Synthesis Rule

File to `synthesis/` when the query:
- Produces a comparison or analysis (not a simple lookup)
- Would take more than 30 seconds to regenerate
- Could be shared with someone else meaningfully

Simple lookups → answer in chat only.

## Token Efficiency

- Load `skills/` and `organisations/` pages before full candidate pages (shorter)
- Use `offset` + `limit` for long files (`log.md`, large sources)
- Do not re-read files already in context this session

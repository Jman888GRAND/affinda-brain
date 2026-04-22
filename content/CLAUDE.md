# Affinda Career Brain — Operating Instructions

This file defines how Claude maintains a career intelligence knowledge base built on the Affinda document AI platform.

---

## Core Idea

The Affinda Career Brain follows the LLM Wiki model:

- Documents are processed via the Affinda API → raw JSON stored in `raw/`
- Knowledge is compiled into structured markdown pages — not re-derived on each query
- Good answers and analyses are filed back into `synthesis/` — nothing disappears into chat
- The graph compounds over time: every new document enriches the whole

---

## Directory Structure

```
AffindaBrain/
├── CLAUDE.md              ← rules (this file)
├── raw/                   ← Affinda API JSON responses (read-only)
├── candidates/            ← one page per candidate
├── jobs/                  ← one page per job description
├── skills/                ← one page per skill (shared graph nodes)
├── organisations/         ← companies, universities, institutions
├── synthesis/             ← filed analyses, match reports, query answers
├── workflow/              ← on-demand workflow instructions
│   ├── ingest.md
│   ├── match.md
│   └── query.md
├── system/
│   └── state.md           ← active session context
├── log.md                 ← append-only operation history
└── index.md               ← master catalog
```

**Rules:**
- Never edit `raw/`
- Claude owns all compiled markdown pages
- Use `workflow/` files only when that workflow is triggered
- Every note must have YAML frontmatter and minimum 2 wikilinks
- Good answers are always filed to `synthesis/` — never left in chat only

---

## Core Workflows

| Workflow | Trigger | File |
|----------|---------|------|
| Ingest | "ingest [document]" | `workflow/ingest.md` |
| Match | "match [candidate] to [job]" | `workflow/match.md` |
| Query | Any question about the graph | `workflow/query.md` |
| Resume | "/resume" | Read `system/state.md` + last 3 `log.md` entries |
| Save | "/save" | Append to `log.md`, update `system/state.md` |

---

## Pipeline

Every document follows this path:

1. **Upload** → Affinda API (`POST https://api.affinda.com/v3/documents`, workspace `avTnlGrd`)
2. **Extract** → JSON response saved to `raw/[filename].json`
3. **Discuss** → summarise key takeaways before writing (don't silently process)
4. **Compile** → markdown page written to `candidates/` or `jobs/`
5. **Link** → wikilinks added to all referenced `skills/` and `organisations/` nodes
6. **Log** → append entry to `log.md`
7. **Update** → `index.md` updated

---

## Frontmatter Standard

Every note must include:

```yaml
---
type: candidate | job | skill | organisation | synthesis
title: [Title]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active | archived
---
```

---

## Graph Principles

- Knowledge is compiled once, not re-derived on each query
- Every skill and organisation is its own atomic page — never embedded only
- Cross-references use `[[Page Name]]` links — every note needs at least 2
- Match analysis always uses three states: ✅ matched / ⚠️ gap / 🔵 hidden
- Do not invent — only write claims from Affinda extraction or explicit user input
- Contradictions are flagged explicitly, never silently overwritten

---

## Synthesis Rule

When a query produces a useful analysis or comparison, file it:
- Write to `synthesis/[descriptive-title].md`
- Link back to the source pages it references
- Add to `index.md`

A match analysis, a skills gap report, a career narrative — these are wiki pages, not chat messages.

---

## Writing Rules

- Concise bullets over prose
- Use `[[links]]` liberally — minimum 2 per note, the graph is the value
- Summarise extracted data — never paste raw JSON
- Mark gaps and hidden skills explicitly, never silently omit them

---

## Token Efficiency

- Never read files speculatively — only read what the task requires
- Read `system/state.md` first each session
- Prefer `skills/` and `organisations/` pages over full candidate pages (shorter)
- Do not re-read files already in context this session
- Use `offset` + `limit` when reading `log.md` (append-only, grows over time)

---

## Session Behavior

Read `system/state.md` only at session start. Then ask:
> "Are we ingesting a document, running a match, or querying the graph?"

**`/resume`** → Read `system/state.md` + last 3 entries in `log.md`. Summarise state and next steps.

**`/save`** → Append session summary to `log.md`. Update `system/state.md`. Include: what was done, decisions made, pending items, links to created/modified pages.

---

## System Principle

> The graph is the memory. The pipeline is the tool. The match is the insight. Synthesis pages are the output.

---

## Schema Evolution

When Claude notices a gap or convention that isn't working, flag it and propose a specific edit. Document every schema change in `log.md`.

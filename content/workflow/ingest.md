# Workflow: Ingest

Triggered by: "ingest [document]"

## Steps

1. **Receive** the document (file path or URL)
2. **Upload** to Affinda API:
   - `POST https://api.affinda.com/v3/documents`
   - Workspace: `avTnlGrd`
   - Auth: Bearer token
3. **Save** raw JSON to `raw/[filename].json`
4. **Discuss** key takeaways before writing — don't silently process
5. **Classify**: resume → `candidates/` · job description → `jobs/`
6. **Compile** page with frontmatter standard (see CLAUDE.md)
7. **Update** all referenced `[[skills/]]` and `[[organisations/]]` nodes
8. **Append** entry to `log.md`
9. **Update** `index.md`

## Frontmatter Template

```yaml
---
type: candidate | job
title: [Title]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

## Rules
- Never edit `raw/` after saving
- Always create skill/org pages even with one connection
- Minimum 2 wikilinks per page
- File useful answers to `synthesis/` — never leave them in chat

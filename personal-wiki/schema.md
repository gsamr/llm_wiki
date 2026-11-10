# Schema — Personal House Wiki

## Purpose
Track everything about the house: the property itself, its systems and appliances, maintenance
history, contractors, warranties, insurance, and renovations — a single place that answers
"what do we know about X" without re-reading the original paperwork.

## Layers
- `raw/sources/` — immutable originals (PDFs, scans, text). Never edit these.
- `wiki/` — markdown pages you (the agent) create and maintain. The only layer you write to.
- `schema.md` (this file) — the rules. Propose edits when a new convention is needed, but ask first.

## Page types and where they live
- `wiki/entities/` — one page per concrete thing: an appliance, a system (HVAC, roof, plumbing),
  a contractor/vendor, an insurance policy. Filename: lowercase-kebab-case, e.g. `entities/hvac-system.md`.
- `wiki/concepts/` — cross-cutting topics, e.g. `concepts/maintenance-history.md`, `concepts/warranties.md`,
  `concepts/renovations.md`.
- `wiki/index.md` — catalog of every page, grouped by category, one line per page with a link and a
  one-sentence summary.
- `wiki/log.md` — append-only. Each entry starts with `## [YYYY-MM-DD] <op> | <title>` where `<op>` is
  `ingest`, `query`, or `lint`.

## Frontmatter
Every wiki page starts with YAML frontmatter:
```yaml
---
title: <page title>
type: entity | concept
tags: [tag1, tag2]
sources: [raw/sources/<file1>, raw/sources/<file2>]
updated: YYYY-MM-DD
---
```

## Language
Source documents may be in Dutch (or other languages). Write all wiki pages in English for
consistency and easy querying, but always quote key original-language terms, clause names, or
figures verbatim alongside the English translation, e.g. `eigen risico ("deductible"): €150`.
This keeps pages traceable to exact original wording for anything legal/financial where precise
phrasing matters. Never silently paraphrase a number, date, or legal term — quote it.

## Conventions
- Use `[[wikilink]]` syntax (page filename without `.md`, no path) to cross-reference other pages.
- When a new source contradicts or supersedes something already in the wiki, don't silently overwrite —
  note the contradiction explicitly on the page (e.g. "Previously listed as a 5-year warranty; the
  2024-03 invoice states 10 years — see Sources.") and flag it in the log entry.
- Keep entity pages factual and sourced. Every claim should be traceable to a source file.
- A single ingest can touch multiple pages (the entity itself, `maintenance-history.md`, `index.md`, `log.md`).

## Operations

### Ingest
1. Read the source with `read_source`.
2. Check `index.md` and relevant existing pages with `list_pages` / `read_page` — don't duplicate what's there.
3. Decide which pages to create or update.
4. Write them with `write_page`, including frontmatter and wikilinks.
5. Update `index.md` to reflect any new or changed pages.
6. Append one entry to `log.md` describing what changed.

### Query
1. Read `index.md` first to find candidate pages.
2. Read the candidate pages with `read_page`.
3. Answer using only what's in those pages, citing page names. If the wiki doesn't have the answer, say
   so — don't guess from source documents you haven't read in this conversation.
4. If the answer is substantial (a comparison or summary worth keeping), consider filing it as a new page
   and note that in the log.

### Lint
1. `list_pages` and read each one.
2. Look for: orphan pages (nothing links to them), pages mentioned in `index.md` that don't exist, stale
   claims contradicted by newer sources, missing obvious cross-references.
3. Report findings. Fix what's safe to fix automatically (e.g. a missing index entry); flag the rest.
4. Append a `log.md` entry summarizing the lint pass.

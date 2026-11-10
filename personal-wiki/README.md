# personal-wiki

A fully local personal knowledge base, following Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
(see also [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) for a full desktop implementation of the
same idea). Drop house-related documents into `raw/sources/`, and a local agent reads them and maintains
a markdown wiki in `wiki/` — entity pages, cross-references, an index, and a log.

Unlike RAG, the LLM doesn't re-derive answers from scratch each query — it incrementally builds and
maintains the wiki, and queries just read from it.

## Architecture

- `raw/sources/` — immutable originals (PDF, txt, md). Never edited by the agent.
- `wiki/` — markdown pages the agent creates/maintains, plus `index.md` (catalog) and `log.md` (history).
- `schema.md` — the rules: page types, frontmatter, conventions, and the ingest/query/lint workflows.
- `agent/` — the Python harness. No orchestration framework: a plain tool-calling loop against an
  OpenAI-compatible chat endpoint.
  - `tools.py` — the only things the model can do: `list_sources`, `read_source`, `list_pages`,
    `read_page`, `write_page`, `append_log`.
  - `loop.py` — the loop itself: send messages + tool schemas, execute any tool calls the model makes,
    feed results back, repeat until the model returns a plain answer.
  - `cli.py` — turns `ingest` / `query` / `lint` into the right instruction for the loop.

## Setup

1. [LM Studio](https://lmstudio.ai/) running locally with its server on (serves an OpenAI-compatible API
   at `http://localhost:1234/v1`), with a model loaded that supports tool calling — this project defaults
   to `qwen/qwen3.6-35b-a3b`. Change `MODEL` in `agent/config.py` if you want a different one.
2. ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

```
source .venv/bin/activate

# drop a file into raw/sources/ first, e.g. raw/sources/hvac-warranty.pdf
python -m agent ingest hvac-warranty.pdf

python -m agent query "When does the HVAC warranty expire?"

python -m agent lint
```

Each run prints every tool call and result as it happens, so you can see exactly what the model reads
and writes — that visibility is the point, not just the output.

## Why this shape

This intentionally skips an agent framework (LangChain, etc.) — the loop in `loop.py` is the whole
"agent": send messages + tool definitions, execute what comes back, repeat. At this scale that's all
tool-calling agents are. Once the wiki grows past what `index.md` can navigate, the natural next step is
adding a `search_wiki` tool backed by local embeddings (e.g. LM Studio's `nomic-embed-text` model) and a
local vector store — but that's deliberately not here yet.

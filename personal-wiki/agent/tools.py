from pypdf import PdfReader

from .config import SOURCES_DIR, WIKI_DIR


def _extract_pdf(path):
    reader = PdfReader(str(path))
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)


def list_sources() -> list[str]:
    return sorted(
        str(p.relative_to(SOURCES_DIR))
        for p in SOURCES_DIR.rglob("*")
        if p.is_file() and p.name != ".gitkeep"
    )


def read_source(filename: str) -> str:
    path = SOURCES_DIR / filename
    if not path.exists():
        return f"ERROR: source not found: {filename}"
    if path.suffix.lower() == ".pdf":
        return _extract_pdf(path)
    return path.read_text(errors="replace")


def list_pages() -> list[str]:
    return sorted(str(p.relative_to(WIKI_DIR)) for p in WIKI_DIR.rglob("*.md"))


def read_page(path: str) -> str:
    full = WIKI_DIR / path
    if not full.exists():
        return f"ERROR: wiki page not found: {path}"
    return full.read_text()


def write_page(path: str, content: str) -> str:
    full = WIKI_DIR / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content)
    return f"wrote {path} ({len(content)} chars)"


def append_log(entry: str) -> str:
    log_path = WIKI_DIR / "log.md"
    with log_path.open("a") as f:
        f.write(entry.rstrip("\n") + "\n")
    return "logged"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_sources",
            "description": "List all files available in raw/sources/.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_source",
            "description": "Read the text content of a file in raw/sources/ (supports .pdf, .md, .txt).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Path relative to raw/sources/"}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_pages",
            "description": "List all existing markdown pages in the wiki.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": "Read an existing wiki page's content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path relative to wiki/, e.g. 'index.md' or 'entities/hvac-system.md'",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_page",
            "description": "Create or overwrite a wiki page with full markdown content, including YAML frontmatter.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path relative to wiki/"},
                    "content": {"type": "string", "description": "Full markdown content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_log",
            "description": (
                "Append one entry to wiki/log.md. Start the entry with "
                "'## [YYYY-MM-DD] <op> | <title>' per schema.md."
            ),
            "parameters": {
                "type": "object",
                "properties": {"entry": {"type": "string"}},
                "required": ["entry"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "list_sources": lambda **kw: list_sources(),
    "read_source": lambda **kw: read_source(kw["filename"]),
    "list_pages": lambda **kw: list_pages(),
    "read_page": lambda **kw: read_page(kw["path"]),
    "write_page": lambda **kw: write_page(kw["path"], kw["content"]),
    "append_log": lambda **kw: append_log(kw["entry"]),
}

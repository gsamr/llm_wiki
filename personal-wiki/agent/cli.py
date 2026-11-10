import sys

from .loop import run

OPS = {
    "ingest": lambda arg: (
        f"Ingest the source file '{arg}' into the wiki. Follow the Ingest workflow in schema.md: "
        "read the source, decide which wiki pages to create or update, write them with proper "
        "frontmatter and [[wikilinks]], update index.md, and append a log.md entry."
    ),
    "query": lambda arg: (
        f"Answer this question using only the wiki: {arg}\n"
        "Read index.md first to find relevant pages, then read those pages before answering. "
        "Cite the wiki pages you used."
    ),
    "lint": lambda arg: (
        "Run a lint pass over the wiki per schema.md's Lint workflow: list all pages, look for "
        "orphan pages, missing cross-references, and contradictions, then report findings "
        "and append a log.md entry."
    ),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in OPS:
        print(f"Usage: python -m agent <{'|'.join(OPS)}> [argument]")
        sys.exit(1)
    op = sys.argv[1]
    arg = " ".join(sys.argv[2:])
    message = OPS[op](arg)
    result = run(message)
    print("\n=== Final answer ===")
    print(result)


if __name__ == "__main__":
    main()

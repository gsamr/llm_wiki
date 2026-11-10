from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "raw" / "sources"
WIKI_DIR = PROJECT_ROOT / "wiki"
SCHEMA_PATH = PROJECT_ROOT / "schema.md"

LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "qwen3.8-27b"
MAX_ITERS = 15

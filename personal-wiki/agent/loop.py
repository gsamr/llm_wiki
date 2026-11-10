import json

from openai import OpenAI

from .config import LM_STUDIO_API_KEY, LM_STUDIO_BASE_URL, MAX_ITERS, MODEL, SCHEMA_PATH
from .tools import TOOL_FUNCTIONS, TOOLS

client = OpenAI(base_url=LM_STUDIO_BASE_URL, api_key=LM_STUDIO_API_KEY)


def _system_prompt() -> str:
    schema = SCHEMA_PATH.read_text()
    return (
        "You are a local agent that maintains a personal wiki from raw source documents. "
        "Use the provided tools to read sources, read/write wiki pages, and log your work. "
        "Follow the conventions and operations below exactly.\n\n"
        f"{schema}"
    )


def run(user_message: str, verbose: bool = True) -> str:
    messages = [
        {"role": "system", "content": _system_prompt()},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_ITERS):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        choice = response.choices[0]
        messages.append(choice.message.model_dump(exclude_none=True))

        if not choice.message.tool_calls:
            return choice.message.content or ""

        for call in choice.message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            if verbose:
                print(f"\n[tool call] {name}({args})")
            try:
                result = TOOL_FUNCTIONS[name](**args)
            except Exception as exc:
                result = f"ERROR: {exc}"
            if verbose:
                preview = str(result)
                print(f"[tool result] {preview[:300]}{'...' if len(preview) > 300 else ''}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})

    return "Stopped: reached max iterations without a final answer."

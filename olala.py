"""A minimal tool-calling loop for Olala 1.0 mini, on any OpenAI-compatible endpoint.

The model answers with tool calls; this loop runs them with your Python functions, sends the results back,
and stops when the model gives a text answer. Settings come from the environment or from a .env file:
OLALA_BASE_URL, OLALA_API_KEY, OLALA_MODEL.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Callable

from openai import OpenAI


def _load_env(path: Path = Path(__file__).with_name(".env")) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#") and value.strip() and key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip().strip("'\"")


_load_env()


def tool(name: str, description: str, **params: str) -> dict:
    """Describe a tool for the model. Each keyword is a required string parameter, with its description."""
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "required": list(params),
                       "properties": {k: {"type": "string", "description": v} for k, v in params.items()}}}}


def run(prompt: str, tools: list[dict] | None = None, functions: dict[str, Callable] | None = None,
        system: str | None = None, max_steps: int = 8, verbose: bool = True) -> str:
    """Ask Olala mini, let it call tools until it answers, and return the answer."""
    client = OpenAI(base_url=os.environ.get("OLALA_BASE_URL", "http://127.0.0.1:8080/v1"),
                    api_key=os.environ.get("OLALA_API_KEY") or "none")
    model = os.environ.get("OLALA_MODEL", "olala")
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    functions = functions or {}
    cut = 0
    for _ in range(max_steps):
        choice = client.chat.completions.create(
            model=model, messages=messages, tools=tools or None, temperature=0.6, top_p=0.95, max_tokens=8192,
            # Olala mini reasons before it answers; "low" is enough for tool use and keeps answers short.
            extra_body={"chat_template_kwargs": {"reasoning_effort": "low", "preserve_thinking": True}},
        ).choices[0]
        reply = choice.message
        if not reply.tool_calls:
            answer = re.sub(r"<think>.*?</think>", "", reply.content or "", flags=re.S).strip()
            if choice.finish_reason == "length" and not answer and cut == 0:
                cut += 1  # the reasoning ran out of room before an answer: ask again once, from the same point
                continue
            return answer or "(no answer: the reply was cut before it ended)"
        messages.append({"role": "assistant", "content": reply.content or "",
                         "tool_calls": [c.model_dump() for c in reply.tool_calls]})
        for call in reply.tool_calls:  # several calls in one reply are fine: Olala mini batches independent work
            args: dict = {}
            try:
                args = json.loads(call.function.arguments or "{}")
                result = functions[call.function.name](**args)
            except Exception as e:  # the model sees the error and can fix its call
                result = f"ERROR: {e}"
            if verbose:
                print(f"  → {call.function.name}({', '.join(f'{k}={v!r}' for k, v in args.items())})")
                print(f"  ← {str(result)[:200]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
    return "(stopped: too many steps)"

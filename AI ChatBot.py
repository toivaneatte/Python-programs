"""Simple command-line chatbot powered by the OpenAI API.

Before running this script, export your API key, for example::

    export OPENAI_API_KEY="sk-..."

Optionally you can set ``OPENAI_MODEL`` to pick a different chat model.
"""

from __future__ import annotations

import os
import sys
from typing import Iterable

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover - defensive guard for missing dependency
    raise SystemExit(
        "The `openai` package is required to run this script. Install it with `pip "
        "install --upgrade openai`."
    ) from exc


def _ensure_api_key() -> str:
    """Return the API key from the environment or exit with a helpful message."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing OpenAI credentials. Set the OPENAI_API_KEY environment variable "
            "before running the chatbot."
        )
    return api_key


def chat_with_gpt(client: OpenAI, prompt: str, model: str) -> str:
    """Send the prompt to the chat model and return the assistant's reply."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    choice = response.choices[0]
    return choice.message.content.strip() if choice.message and choice.message.content else ""


def _iter_user_prompts(exit_commands: Iterable[str]) -> Iterable[str]:
    """Yield prompts from stdin until the user types one of ``exit_commands``."""

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()  # newline for cleanliness
            return
        if user_input.lower().strip() in exit_commands:
            return
        yield user_input


def main() -> int:
    client = OpenAI(api_key=_ensure_api_key())
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    exit_commands = {"quit", "exit", "q"}

    for prompt in _iter_user_prompts(exit_commands):
        try:
            reply = chat_with_gpt(client, prompt, model=model)
        except Exception as exc:  # pragma: no cover - surface API errors to the user
            print(f"Chatbot: (virhe) {exc}", file=sys.stderr)
            continue
        print("Chatbot:", reply)

    print("Chatbot: Näkemiin!")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry-point
    sys.exit(main())

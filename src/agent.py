"""
Context Hub — Demo Agent

A minimal agent that uses fetch_context to pull relevant context from the
Twilio Context Hub before answering a user query.

Usage:
    python src/agent.py
"""

import json
import os
import httpx
import anthropic

from config import FETCH_CONTEXT_ENDPOINT, CONTEXT_HUB_API_KEY, CONTEXT_HUB_TIMEOUT

ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def fetch_context(query: str, sources: list[str] | None = None) -> dict:
    """Call the Context Hub to retrieve ranked context for *query*.

    Args:
        query:   The natural-language question the agent is trying to answer.
        sources: Optional list of provider names to restrict the lookup, e.g.
                 ["salesforce", "google_calendar"].  When omitted the hub uses
                 all configured providers.

    Returns:
        A dict with a ``context`` list of ranked context snippets.
    """
    payload: dict = {"query": query}
    if sources:
        payload["sources"] = sources

    headers = {
        "Authorization": f"******",
        "Content-Type": "application/json",
    }

    response = httpx.post(
        FETCH_CONTEXT_ENDPOINT,
        json=payload,
        headers=headers,
        timeout=CONTEXT_HUB_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def run_agent(user_query: str) -> str:
    """Run a single-turn agent that enriches its answer with hub context.

    The agent first fetches relevant context from the hub, then passes that
    context alongside the user query to Claude to produce a final answer.
    """
    print(f"[agent] Fetching context for: {user_query!r}")
    ctx_response = fetch_context(user_query)
    context_snippets: list[str] = [
        item.get("text", "") for item in ctx_response.get("context", [])
    ]
    context_block = "\n\n".join(context_snippets)

    system_prompt = (
        "You are a helpful assistant. "
        "Use the context below (retrieved from the user's connected data sources) "
        "to answer the question accurately.\n\n"
        f"<context>\n{context_block}\n</context>"
    )

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_query}],
    )

    answer: str = message.content[0].text
    print(f"[agent] Answer: {answer}")
    return answer


if __name__ == "__main__":
    sample_query = "What meetings do I have tomorrow and are there any open deals I should prepare for?"
    run_agent(sample_query)

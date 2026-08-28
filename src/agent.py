"""
Sample agent that uses Context Hub for intelligent tool routing.

Instead of loading 600+ tools from 19 providers, the agent loads ONE tool:
fetch_context(query). Context Hub handles routing, tool selection, and execution.
"""

import os
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

HUB_MCP_URL = os.environ.get("CONTEXT_HUB_MCP_ENDPOINT", "http://localhost:8000/mcp")

SYSTEM_PROMPT = """You are a helpful personal assistant with access to enterprise tools
via the Twilio Context Hub.

For any question about work data — email, calendar, messages, SMS, code, tickets, docs —
call fetch_context with a clear, specific query. The Hub will route to the right provider
and return the data you need.

Never guess at data you don't have. Always call fetch_context first."""


def run_query(message: str, hub_headers: dict = None):
    """Run a single query through the Hub."""
    headers = hub_headers or {}

    with MCPClient(url=HUB_MCP_URL, headers=headers) as client:
        tools = client.list_tools_sync()

        agent = Agent(
            model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )

        result = agent(message)
        return str(result)


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "What's on my calendar today?"
    print(f"Query: {query}\n")
    print(run_query(query))

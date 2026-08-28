"""Sample agent consumer app."""

import os
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

HUB_MCP_URL = os.environ.get("HUB_MCP_URL", "https://your-hub.example.com/mcp")

def run_query(message: str, headers: dict = None):
    with MCPClient(url=HUB_MCP_URL, headers=headers or {}) as client:
        agent = Agent(
            model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
            tools=client.list_tools_sync(),
        )
        return str(agent(message))

if __name__ == "__main__":
    import sys
    print(run_query(" ".join(sys.argv[1:]) or "hello"))

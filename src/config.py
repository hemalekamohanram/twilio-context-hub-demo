"""
Configuration for the Context Hub demo app.
"""

import os

# Context Hub endpoints
HUB_SERVER_URL = os.environ.get("CREDENTIALS_ENDPOINT", "https://your-hub-server.example.com")
HUB_MCP_URL = os.environ.get("CONTEXT_HUB_MCP_ENDPOINT", f"{HUB_SERVER_URL}/mcp")
AGENT_ENDPOINT = os.environ.get("PERSONAL_AGENT_ENDPOINT", "https://your-agent.example.com")
INTEGRATIONS_URL = os.environ.get("INTEGRATIONS_BASE_URL", "https://your-integrations.example.com")

# Supported providers (19 live)
PROVIDERS = {
    "communication": ["gmail", "googleCalendar", "slack", "zoom", "twilioMemory"],
    "productivity": ["googleDrive", "googleDocs", "notion"],
    "engineering": ["github", "jira", "confluence"],
    "crm": ["salesforce", "hubspot"],
    "support": ["zendesk", "servicenow", "pagerduty"],
    "data": ["snowflake", "bigquery", "twilioKnowledge"],
    "platform": ["twilio"],
    "research": ["webSearch"],
    "ai": ["anthropic"],
}

TOTAL_TOOLS = 72
TOTAL_PROVIDERS = 19
TOTAL_CATEGORIES = 9

"""
Configuration for the Context Hub demo app.
"""

import os

# Context Hub endpoints
HUB_SERVER_URL = os.environ.get("CREDENTIALS_ENDPOINT", "http://localhost:8000")
HUB_MCP_URL = os.environ.get("CONTEXT_HUB_MCP_ENDPOINT", f"{HUB_SERVER_URL}/mcp")
AGENT_ENDPOINT = os.environ.get("PERSONAL_AGENT_ENDPOINT", "http://localhost:8080")
INTEGRATIONS_URL = os.environ.get("INTEGRATIONS_BASE_URL", "http://localhost:8082")

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

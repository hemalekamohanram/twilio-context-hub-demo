"""
Salesforce MCP provider — accounts, opportunities, contacts.

Auth: Admin-configured shared credentials (X-Developer-Id header).
The combined-mcp server reads tenant-level secrets from AWS Secrets Manager.
"""

SALESFORCE_TOOLS = [
    "search_accounts",      # Search Salesforce accounts by name or domain
    "list_opportunities",   # List open sales opportunities with stage filtering
    "get_account",          # Get detailed account info by ID
]

# TODO: Add lead scoring integration
# TODO: Add Salesforce report generation

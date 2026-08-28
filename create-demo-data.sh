#!/usr/bin/env bash
# create-demo-data.sh
# Run this script locally (after `gh auth login`) to create the demo issues and PRs.
# Usage: bash create-demo-data.sh

set -euo pipefail

REPO="hemalekamohanram/twilio-context-hub-demo"

echo "=== Creating demo issues ==="

gh issue create \
  --repo "$REPO" \
  --title "[Feature] Add Twilio Memory as a data source" \
  --body "## Summary

Add Twilio Memory as a context provider in the hub. When a user query is processed, the hub should pull from stored memory snippets (e.g. past preferences, prior interactions) and rank them alongside other sources.

## Acceptance Criteria

- [ ] Implement \`TwilioMemoryProvider\` in \`src/\`
- [ ] Register the provider in the hub routing config
- [ ] Add unit tests
- [ ] Update \`docs/architecture.md\`"

gh issue create \
  --repo "$REPO" \
  --title "[Bug] Direct mode crashes with duplicate tool names" \
  --body "## Description

When the hub is configured in direct mode and two providers register tools with the same name, the agent crashes with an \`AssertionError\`.

## Steps to Reproduce

1. Configure two providers that both expose a \`search\` tool.
2. Send any query in direct mode.
3. Observe the crash.

## Expected Behaviour

The hub should either deduplicate tool names or raise a clear, recoverable error."

gh issue create \
  --repo "$REPO" \
  --title "[Feature] Add web search provider for date awareness" \
  --body "## Summary

The hub currently has no way to retrieve real-time information such as the current date or recent events. Adding a web search provider would allow the agent to answer date-sensitive queries accurately.

## Acceptance Criteria

- [ ] Implement \`WebSearchProvider\` backed by a configurable search API (e.g. Brave, Serper)
- [ ] Register the provider and add routing hints for date / news queries
- [ ] Update \`docs/architecture.md\`"

echo ""
echo "=== Creating demo PRs ==="

# PR 1 — Salesforce integration
git checkout -b feature/salesforce-integration main 2>/dev/null || git checkout feature/salesforce-integration
mkdir -p src
cat > src/salesforce_provider.py << 'EOF'
"""Salesforce CRM provider for Context Hub."""

import os
import httpx

SALESFORCE_INSTANCE_URL = os.environ.get("SALESFORCE_INSTANCE_URL", "")
SALESFORCE_ACCESS_TOKEN = os.environ.get("SALESFORCE_ACCESS_TOKEN", "")


def fetch_salesforce_context(query: str) -> list[dict]:
    """Search Salesforce for records relevant to *query*."""
    headers = {"Authorization": f"******"}
    sosl = f"FIND {{{query}}} IN ALL FIELDS RETURNING Account, Opportunity, Contact"
    url = f"{SALESFORCE_INSTANCE_URL}/services/data/v59.0/search/"
    response = httpx.get(url, params={"q": sosl}, headers=headers, timeout=10)
    response.raise_for_status()
    return [
        {"source": "salesforce", "score": 0.9, "text": str(r)}
        for r in response.json().get("searchRecords", [])
    ]
EOF
git add src/salesforce_provider.py
git commit -m "Add Salesforce integration to Context Hub"
git push origin feature/salesforce-integration
gh pr create \
  --repo "$REPO" \
  --base main \
  --head feature/salesforce-integration \
  --title "Add Salesforce integration to Context Hub" \
  --body "Adds a Salesforce CRM provider to Context Hub.

## Changes
- New \`src/salesforce_provider.py\` with SOSL-based record search

## Type of Change
- [x] New feature / provider

## Testing
- [ ] Unit tests to be added in a follow-up PR
"

# PR 2 — OAuth token refresh fix
git checkout -b fix/oauth-token-refresh main 2>/dev/null || git checkout fix/oauth-token-refresh
cat > src/google_calendar_provider.py << 'EOF'
"""Google Calendar provider for Context Hub."""

import os
import time
import httpx

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")

_access_token: str = ""
_token_expiry: float = 0.0


def _refresh_access_token() -> str:
    """Exchange the refresh token for a new access token."""
    global _access_token, _token_expiry
    resp = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
        timeout=10,
    )
    resp.raise_for_status()
    payload = resp.json()
    _access_token = payload["access_token"]
    _token_expiry = time.time() + payload.get("expires_in", 3600) - 60
    return _access_token


def _get_access_token() -> str:
    if not _access_token or time.time() >= _token_expiry:
        return _refresh_access_token()
    return _access_token


def fetch_calendar_context(query: str) -> list[dict]:
    """Return upcoming calendar events relevant to *query*."""
    token = _get_access_token()
    resp = httpx.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers={"Authorization": f"******"},
        params={"q": query, "maxResults": 5, "orderBy": "startTime", "singleEvents": "true"},
        timeout=10,
    )
    resp.raise_for_status()
    return [
        {"source": "google_calendar", "score": 0.85, "text": str(e)}
        for e in resp.json().get("items", [])
    ]
EOF
git add src/google_calendar_provider.py
git commit -m "Fix: OAuth token refresh for Google Calendar"
git push origin fix/oauth-token-refresh
gh pr create \
  --repo "$REPO" \
  --base main \
  --head fix/oauth-token-refresh \
  --title "Fix: OAuth token refresh for Google Calendar" \
  --body "Fixes silent token expiry in the Google Calendar provider.

## Changes
- New \`src/google_calendar_provider.py\` with automatic token refresh

## Type of Change
- [x] Bug fix

## Testing
- [ ] Manual test with expired token confirmed refresh works
"

# PR 3 — Routing model upgrade
git checkout -b chore/upgrade-routing-model main 2>/dev/null || git checkout chore/upgrade-routing-model
sed -i 's/claude-opus-4-5/claude-opus-4-5/' src/agent.py  # placeholder change to create a diff
git add src/agent.py
git commit -m "Upgrade routing model from Sonnet to Opus 5"
git push origin chore/upgrade-routing-model
gh pr create \
  --repo "$REPO" \
  --base main \
  --head chore/upgrade-routing-model \
  --title "Upgrade routing model from Sonnet to Opus 5" \
  --body "Upgrades the intent-classification model used by the hub router from Claude Sonnet to Claude Opus 5 for improved provider selection accuracy.

## Changes
- Update model reference in \`src/agent.py\`

## Type of Change
- [x] Refactor / performance improvement
"

git checkout main
echo ""
echo "=== Done! ==="
echo "Issues and PRs have been created in $REPO."

"""
Fix: Google OAuth refresh token race condition.

When multiple Google services (Calendar, Drive, Docs) share one OAuth client,
the fetcher's first-hit-wins lookup could pick a stale single-scope token
over a newly-connected all-scope token.

Fix: connections.complete_connection() now writes the fresh token to the
canonical 'gmail' key whenever ANY Google service completes OAuth.
"""

GOOGLE_OAUTH_GROUP = frozenset({
    "gmail", "googleCalendar", "googleDrive", "googleDocs", "googleMeet"
})

def on_google_connect(provider: str, tokens: dict):
    """Always refresh the canonical gmail key with the latest all-scope token."""
    store_token(provider, tokens)
    if provider in GOOGLE_OAUTH_GROUP:
        store_token("gmail", tokens)  # canonical key the fetcher checks first

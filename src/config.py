"""
Context Hub — endpoint configuration.

Set the following environment variables before running the agent:

  CONTEXT_HUB_BASE_URL   Base URL of the Context Hub service
                         e.g. https://context-hub.twilio.com
  CONTEXT_HUB_API_KEY    API key issued by Twilio Console
  CONTEXT_HUB_TIMEOUT    Request timeout in seconds (default: 10)
"""

import os

CONTEXT_HUB_BASE_URL: str = os.environ.get(
    "CONTEXT_HUB_BASE_URL", "https://context-hub.twilio.com"
)
CONTEXT_HUB_API_KEY: str = os.environ.get("CONTEXT_HUB_API_KEY", "")
CONTEXT_HUB_TIMEOUT: int = int(os.environ.get("CONTEXT_HUB_TIMEOUT", "10"))

FETCH_CONTEXT_ENDPOINT: str = f"{CONTEXT_HUB_BASE_URL}/v1/context/fetch"

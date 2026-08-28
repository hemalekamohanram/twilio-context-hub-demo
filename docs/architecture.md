# Context Hub — Architecture

## Overview

Context Hub is a lightweight routing and aggregation service that sits between an AI agent and the data sources it needs to query.  The agent sends a single `fetch_context` request; the hub fans the request out to every relevant provider, ranks the returned snippets by relevance, and returns a unified context window.

## Routing Diagram

```
┌─────────────────────────────────────────────────────────┐
│                        Agent                            │
│  (src/agent.py — calls fetch_context with user query)   │
└───────────────────────┬─────────────────────────────────┘
                        │  POST /v1/context/fetch
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   Context Hub                           │
│                                                         │
│  1. Parse query intent                                  │
│  2. Select providers (routing model)                    │
│  3. Fan-out requests to providers                       │
│  4. Rank & deduplicate snippets                         │
│  5. Return ranked context list                          │
└──┬──────────┬──────────┬──────────┬─────────────────────┘
   │          │          │          │
   ▼          ▼          ▼          ▼
Salesforce  Google   Twilio    Web Search
  CRM      Calendar  Memory    (planned)
```

## Components

### Agent (`src/agent.py`)

- Accepts a natural-language query from the user.
- Calls `fetch_context(query)` to retrieve ranked snippets from the hub.
- Passes the snippets as a system-prompt context block to Claude.
- Returns the model's answer to the user.

### Config (`src/config.py`)

Reads hub endpoint and credentials from environment variables:

| Variable | Description | Default |
|---|---|---|
| `CONTEXT_HUB_BASE_URL` | Base URL of the hub service | `https://context-hub.twilio.com` |
| `CONTEXT_HUB_API_KEY` | API key from Twilio Console | *(required)* |
| `CONTEXT_HUB_TIMEOUT` | HTTP timeout in seconds | `10` |

### Context Hub Service

The hub exposes a single REST endpoint:

```
POST /v1/context/fetch
Authorization: ******

{
  "query": "string",
  "sources": ["salesforce", "google_calendar"]   // optional filter
}
```

Response:

```json
{
  "context": [
    { "source": "salesforce", "score": 0.92, "text": "..." },
    { "source": "google_calendar", "score": 0.87, "text": "..." }
  ]
}
```

## Routing Model

The hub uses a lightweight intent-classification model (currently Claude Sonnet) to decide which providers to query for a given request.  The model is prompted with a description of each configured provider and the user query; it returns a ranked list of providers to fan the request out to.

> **Upcoming:** [#3 Upgrade routing model from Sonnet to Opus 5](https://github.com/hemalekamohanram/twilio-context-hub-demo/pull/3)

## Planned Providers

| Provider | Status | Notes |
|---|---|---|
| Salesforce CRM | ✅ Available | OAuth 2.0 client credentials |
| Google Calendar | ✅ Available | OAuth 2.0 with token refresh |
| Twilio Memory | 🔜 Planned | See [Issue #1](https://github.com/hemalekamohanram/twilio-context-hub-demo/issues/1) |
| Web Search | 🔜 Planned | See [Issue #3](https://github.com/hemalekamohanram/twilio-context-hub-demo/issues/3) |

## Known Issues

- [Bug #2: Direct mode crashes with duplicate tool names](https://github.com/hemalekamohanram/twilio-context-hub-demo/issues/2)

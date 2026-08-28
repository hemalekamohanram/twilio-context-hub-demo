# Context Hub — Routing Architecture

## The Problem

An LLM can hold ~80 tools before selection quality collapses.
20 MCP providers × ~30 tools each = 600+ tools.

Every AI agent team at Twilio independently builds:
- Tool routing (which provider to call?)
- Credential management (how to auth to each provider?)
- Context optimization (how to fit tools in the prompt?)

## The Solution: 3-Stage Intelligent Routing

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Stage 1        │    │  Stage 2         │    │  Stage 3        │
│  Category Router│───▶│  MCP Selector    │───▶│  Vector Search  │
│                 │    │                  │    │                 │
│  8 categories   │    │  1-3 MCPs from   │    │  2-5 specific   │
│  Sonnet (~1s)   │    │  candidates      │    │  tools via      │
│                 │    │  Sonnet (~1s)    │    │  Titan embed.   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Categories

| Category | Providers |
|---|---|
| Communication | Gmail, Calendar, Slack, Zoom, Twilio Memory |
| Productivity | Drive, Docs, Notion |
| Engineering | GitHub, Jira, Confluence |
| CRM | Salesforce, HubSpot |
| Support | Zendesk, ServiceNow, PagerDuty |
| Data | Snowflake, BigQuery, Twilio Knowledge |
| Platform | Twilio (SMS, Calls, Numbers) |
| Research | Web Search (DuckDuckGo) |
| AI | Anthropic Claude |

## Security: Zero-Trust Credential Model

1. Credentials NEVER enter the LLM context or system prompt
2. Identity travels as transport headers (X-User-Token, Authorization)
3. Multi-tenant isolation: developer → app → user → provider
4. OAuth apps registered at tenant level, not per-user
5. End users connect their own accounts via Hub's connect page

## Result

- 90-98% fewer tokens per query
- 2-5 tools loaded instead of 72
- Accurate tool selection (no hallucinated tool calls)
- Sub-second routing overhead

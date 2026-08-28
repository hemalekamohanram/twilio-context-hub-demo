# Twilio Context Hub — Demo Consumer App

A sample AI assistant built on **Twilio Context Hub**, demonstrating how a single
`fetch_context(query)` call replaces loading 600+ tools into an LLM's context window.

## What This App Does

This is the "assistant app" — a personal work assistant for Twilio employees.
It connects to 19 data sources (Gmail, Calendar, GitHub, Slack, Twilio, Jira, etc.)
through Context Hub's intelligent routing layer.

## Architecture

```
User query: "Summarize my emails and check my GitHub PRs"
    │
    ▼
Assistant Agent (Claude Sonnet)
    │
    │  fetch_context(query)   ← ONE tool call
    ▼
Context Hub (routes intelligently)
    ├── Stage 1: Category Router  → [Communication, Engineering]
    ├── Stage 2: MCP Selector     → [Gmail, GitHub]
    └── Stage 3: Vector Retrieval → [search_gmail, list_pull_requests]
                                     2 tools loaded (not 72)
```

## Quick Start

```bash
# Prerequisites: AWS SSO, Python 3.12, uv
aws sso login --profile cnd-tweek14-07-sandbox-admin

# One command — starts all 5 services
make local-all

# Open in browser
open http://localhost:8501   # Agent UI
open http://localhost:8502   # Hub Admin UI
```

## Key Metrics

| Metric | Value |
|---|---|
| Total providers | 19 live |
| Total tools indexed | 72 |
| Tools loaded per query | 2-5 |
| Token reduction | 90-98% |
| Routing | 3-stage: Category → MCP → Tool (vector) |
| Auth | Zero-trust, transport headers only |

## Team

- **Hemaleka Mohanram** — Agent integration, UI, MCP providers
- **Dinesh Maheshwari** — Identity architecture, routing, deployment

Built for **H.O.O.T. Hackathon 2026** 🦉

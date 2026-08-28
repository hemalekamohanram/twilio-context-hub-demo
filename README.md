# Context Hub — Demo App

A demonstration of Twilio's Context Hub: a unified routing layer that fetches relevant context from multiple data sources (CRM, calendar, memory, etc.) and surfaces it to an AI agent at inference time.

## Overview

Context Hub sits between your AI agent and the various systems it needs to query. Instead of hard-coding tool calls for every data source, the agent asks the hub for context and the hub routes the request to the right provider, aggregates the results, and returns a ranked context window.

```
Agent  ──►  Context Hub  ──►  Salesforce
                         ──►  Google Calendar
                         ──►  Twilio Memory
                         ──►  Web Search
```

## Project Structure

```
context-hub-demo/
├── README.md
├── requirements.txt
├── src/
│   ├── agent.py        # Simple agent that calls fetch_context
│   └── config.py       # Hub endpoint configuration
├── docs/
│   └── architecture.md # Routing diagram and design notes
└── .github/
    └── PULL_REQUEST_TEMPLATE.md
```

## Quickstart

```bash
pip install -r requirements.txt
python src/agent.py
```

## Configuration

Copy `src/config.py` and set the environment variables listed there before running the agent.

## Contributing

See [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) for contribution guidelines.

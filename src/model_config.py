"""
Tiered model strategy — fast models for routing, strong model for execution.

Before: Opus 5 for everything (slow, expensive)
After:  Sonnet for routing/planning, Opus only for tool execution

Expected: ~5-8s faster per query
"""

ORCHESTRATION_MODEL = "us.anthropic.claude-opus-5"          # tool execution (quality)
FAST_MODEL          = "us.anthropic.claude-sonnet-4-5-v2"   # routing + chat (speed)

# Who uses what:
# router.py          → FAST_MODEL (classification)
# tool_retrieval.py  → FAST_MODEL (query rewriting)
# chat_agent.py      → FAST_MODEL (response formatting)
# fetcher.py         → ORCHESTRATION_MODEL (tool calling — needs quality)

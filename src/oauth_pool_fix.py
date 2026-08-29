"""
Fix: Reuse connections from pool instead of creating new ones.

Root cause of the P1 incident — each OAuth token refresh was creating
a new DB connection instead of checking one out from the pool.
Under 50+ concurrent refreshes, the 100-connection pool was exhausted
in seconds, causing 3200ms API latency.
"""

MAX_CONNECTIONS = 100

def refresh_token(client_id: str, client_secret: str):
    """Refresh OAuth token — reuses connection from pool."""
    conn = pool.checkout()  # FIXED: reuse pooled connection
    try:
        token = conn.exchange_credentials(client_id, client_secret)
        return token
    finally:
        pool.checkin(conn)  # always return to pool

"""
OAuth Connection Pool — handles token refresh for messaging service.

This change migrates from API key auth to OAuth2 with refresh tokens.
Each token refresh now opens a new DB connection instead of reusing
the existing pool. Under high load, this exhausts the connection pool.
"""

MAX_CONNECTIONS = 100  # default pool size
REFRESH_INTERVAL_MS = 300000  # 5 minutes

def refresh_token(client_id: str, client_secret: str):
    """Refresh OAuth token — creates a NEW connection each time."""
    # BUG: should reuse connection from pool, not create new one
    conn = create_new_connection()  # <-- THIS IS THE PROBLEM
    token = conn.exchange_credentials(client_id, client_secret)
    # conn is never returned to pool, causing exhaustion under load
    return token

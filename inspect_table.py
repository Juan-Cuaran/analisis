import sqlite3
from pathlib import Path
path = Path('db.sqlite3')
with sqlite3.connect(path) as conn:
    cur = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='token_blacklist_outstandingtoken'")
    row = cur.fetchone()
    print(row[0] if row else 'no table')

import sqlite3
from pathlib import Path
path = Path('db.sqlite3')
with sqlite3.connect(path) as conn:
    cur = conn.execute("SELECT app, name FROM django_migrations WHERE app = 'token_blacklist'")
    print(list(cur.fetchall()))

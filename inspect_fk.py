import sqlite3
from pathlib import Path
path = Path('db.sqlite3')
print('db exists', path.exists())
with sqlite3.connect(path) as conn:
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.execute("PRAGMA foreign_key_list('token_blacklist_outstandingtoken')")
    print('foreign keys:')
    for row in cur.fetchall():
        print(row)
    print('tables:')
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        print(row[0])

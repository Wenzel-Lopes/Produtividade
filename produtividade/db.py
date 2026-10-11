import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Database:
    def __init__(self, path="data/warehouse.sqlite", postgres=False):
        self.postgres = postgres
        if postgres:
            import psycopg
            from psycopg.rows import dict_row
            self.conn = psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)
        else:
            if str(path) != ":memory:":
                Path(path).parent.mkdir(parents=True,exist_ok=True)
            self.conn = sqlite3.connect(path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys=ON")
        for statement in (ROOT/"sql/001_schema.sql").read_text(encoding="utf-8").split(";"):
            if statement.strip():
                self.conn.execute(statement)
        self.conn.commit()

    def execute(self, query, params=()):
        return self.conn.execute(query.replace("?","%s") if self.postgres else query,params)

    def rows(self, query, params=()):
        return [dict(r) for r in self.execute(query,params).fetchall()]

    def close(self):
        self.conn.close()

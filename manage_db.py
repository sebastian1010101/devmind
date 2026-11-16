"""Explicit PostgreSQL setup and non-destructive import of legacy SQLite data."""

import argparse
import os
import sqlite3
import tempfile
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
import psycopg
from psycopg import sql

from learning_store import LearningStore

TABLES = ["learners", "cards", "card_evidence", "review_schedule", "operations", "review_events",
          "study_sessions", "daily_assignments", "daily_usage", "provider_runs"]


def migrate(url):
    with psycopg.connect(url, connect_timeout=10) as db:
        db.execute("SELECT pg_advisory_xact_lock(67245812)")
        exists = db.execute("SELECT to_regclass('devmind.schema_version')").fetchone()[0]
        if exists:
            version = db.execute("SELECT max(version) FROM devmind.schema_version").fetchone()[0]
            if version == 2:
                print("PostgreSQL já está na versão 2.")
                return
            raise RuntimeError("Versão inesperada. Revise as migrações antes de continuar.")
        db.execute(Path("migrations/003_postgres.sql").read_text(), prepare=False)
    print("Schema privado devmind criado na versão 2.")


def import_sqlite(url, source, owner=None):
    if owner:
        owner = str(UUID(owner))
    if not source.is_file():
        raise RuntimeError("SQLite de origem não encontrado.")
    # Backup API takes a consistent snapshot including any WAL, preserving the source.
    with tempfile.TemporaryDirectory() as directory:
        snapshot = Path(directory) / "snapshot.sqlite3"
        with sqlite3.connect(f"file:{source.resolve()}?mode=ro", uri=True) as src, sqlite3.connect(snapshot) as dst:
            src.backup(dst)
        LearningStore(snapshot)
        with sqlite3.connect(snapshot) as src, psycopg.connect(url, connect_timeout=10) as dst:
            src.row_factory = sqlite3.Row
            dst.execute("SET LOCAL search_path TO devmind, pg_catalog")
            dst.execute("SELECT pg_advisory_xact_lock(67245812)")
            if any(dst.execute(sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table))).fetchone()[0] for table in TABLES if table != "learners"):
                raise RuntimeError("O destino deve estar vazio. A importação foi cancelada sem gravar dados.")
            for table in TABLES:
                columns = [row[1] for row in src.execute(f"PRAGMA table_info({table})")]
                query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table), sql.SQL(",").join(map(sql.Identifier, columns)),
                    sql.SQL(",").join(sql.Placeholder() for _ in columns),
                )
                if table == "learners":
                    query += sql.SQL(" ON CONFLICT(id) DO NOTHING")
                order = " ORDER BY rowid" if table in {"operations", "review_events"} else ""
                for row in src.execute(f"SELECT * FROM {table}{order}"):
                    values = dict(row)
                    field = "id" if table == "learners" else "user_id"
                    if owner and values.get(field) == "local-demo":
                        values[field] = owner
                    dst.execute(query, tuple(values[column] for column in columns))
    print("Importação concluída em uma transação. O SQLite original foi preservado.")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["migrate", "import-sqlite"])
    parser.add_argument("--source", type=Path, default=Path("data/learning.sqlite3"))
    parser.add_argument("--owner", help="UUID Supabase que receberá exclusivamente os dados local-demo")
    args = parser.parse_args()
    url = os.getenv("DATABASE_URL")
    if not url:
        parser.error("Configure DATABASE_URL no ambiente.")
    try:
        if args.command == "migrate":
            migrate(url)
        else:
            import_sqlite(url, args.source, args.owner)
    except (psycopg.Error, RuntimeError, ValueError) as exc:
        # Provider/database exceptions can include credentials or private row data.
        parser.exit(1, f"Operação cancelada ({type(exc).__name__}). Revise conexão, destino e documentação de migração.\n")


if __name__ == "__main__":
    main()

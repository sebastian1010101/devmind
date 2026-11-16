"""Small DB-API adapter for the existing transactional learning repository."""

from contextlib import contextmanager
import re

import psycopg

from providers import ServiceError


class Row(dict):
    def __init__(self, names, values):
        super().__init__(zip(names, values))
        self.values_tuple = values

    def __getitem__(self, key):
        return self.values_tuple[key] if isinstance(key, int) else super().__getitem__(key)


def row_factory(cursor):
    names = [column.name for column in cursor.description] if cursor.description else []
    return lambda values: Row(names, values)


class Database:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, query, params=()):
        # All queries and field names are static application SQL.
        query = query.replace("?", "%s")
        query = re.sub(r"\browid\b", "ordinal", query)
        return self.connection.execute(query, params)


@contextmanager
def postgres_connection(url, user_id, write):
    try:
        with psycopg.connect(url, connect_timeout=5, row_factory=row_factory) as connection:
            connection.execute("SET LOCAL search_path TO devmind, pg_catalog")
            connection.execute("SET LOCAL statement_timeout='10000ms'")
            connection.execute("SELECT set_config('app.user_id', %s, true)", (user_id,))
            if write:
                # All writers reserve budgets and leases in the same lock order.
                connection.execute("SELECT pg_advisory_xact_lock(67245812)")
            yield Database(connection)
    except psycopg.Error:
        raise ServiceError("database_unavailable", "A base de dados está indisponível. Verifique a conexão e as migrações.", 503) from None

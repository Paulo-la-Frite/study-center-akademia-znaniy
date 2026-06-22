"""Модуль для работы с базой данных PostgreSQL."""
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from src.config import DB_CONFIG


@contextmanager
def get_connection():
    """Контекстный менеджер для соединения с БД."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """Выполняет SQL-запрос с параметризацией (защита от инъекций)."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            conn.commit()
            return None
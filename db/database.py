from abc import ABC, abstractmethod
from typing import Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import PostgresSettings

config = PostgresSettings()


class AbstractDataBase(ABC):

    @abstractmethod
    async def get_user(self, record_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    async def get_all_users(self) -> Dict:
        pass


class PostgresDataBase(AbstractDataBase):
    """
    Класс для соединения и запросов к postgres
    """
    def __init__(self):
        self.dsn = config.dict()
        self._connection = None
        self._cursor = None

    def close(self):
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
        self._connection = None
        self._cursor = None

    def get_all_users(self):
        query = """
        SELECT * FROM users;
        """
        return self._pg_execute_all(query)

    def get_user(self, user_id):
        query = """
        SELECT * FROM users WHERE id = '{user_id}';
        """.format(user_id=user_id)
        return self._pg_execute_one(query)

    def _pg_execute_all(self, query):
        with psycopg2.connect(**self.dsn, cursor_factory=RealDictCursor) as self._connection:
            with self._connection.cursor() as self._cursor:
                self._cursor.execute(query)
                return self._cursor.fetchall()

    def _pg_execute_one(self, query):
        with psycopg2.connect(**self.dsn, cursor_factory=RealDictCursor) as self._connection:
            with self._connection.cursor() as self._cursor:
                self._cursor.execute(query)
                return self._cursor.fetchone()


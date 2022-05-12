from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from typing import Dict
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import PostgresSettings

config = PostgresSettings()


class AbstractDataBase(ABC):

    @abstractmethod
    def get_user(self, record_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_users(self) -> Dict:
        pass

    @abstractmethod
    def update_user(self, user_id) -> None:
        pass


class PostgresDataBase(AbstractDataBase):
    """
    Класс для соединения и запросов к postgres
    """
    def __init__(self):
        self.dsn = config.dict()
        self.connection = self._connection()
        self.cursor = self._cursor()

    def _connection(self):
        return psycopg2.connect(**self.dsn, cursor_factory=RealDictCursor)

    def _cursor(self):
        return self.connection.cursor()

    def close(self):
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
        self.connection = None
        self.cursor = None

    def get_user(self):
        pass

    def get_all_users(self):
        query = """
        SELECT * FROM users;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_user(self, user_id):
        query = """
        UPDATE users SET email_verified=true WHERE id = '{user_id}';
        """.format(user_id=user_id)
        self.cursor.execute(query)
        self.connection.commit()
        self.close()


@lru_cache()
def get_db_service() -> PostgresDataBase:
    return PostgresDataBase()

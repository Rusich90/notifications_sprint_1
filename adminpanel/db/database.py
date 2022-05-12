from abc import ABC, abstractmethod
from typing import Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from config.settings import PostgresSettings
from config.logger_config import LOGGING_CONFIG
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app')
MAX_ROW = 10000

config = PostgresSettings()


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        def inner(*args, **kwargs):
            t = start_sleep_time
            while t <= border_sleep_time:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception('Database error', e)
                    t = t * factor
                    sleep(t)

        return inner

    return func_wrapper


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

    @backoff(0.2, 2, 10)
    def _pg_execute_all(self, query):
        with psycopg2.connect(**self.dsn, cursor_factory=RealDictCursor) as self._connection:
            with self._connection.cursor() as self._cursor:
                fullresult = []
                self._cursor.execute(query)
                while True :
                    initial_list = self._cursor.fetchmany(size=MAX_ROW)
                    if not initial_list:
                        return fullresult
                    fullresult = fullresult + initial_list
                    if len(initial_list) < MAX_ROW :
                        break
                logger.info("Из базы скачано {}  уникальных пользователей".format(
                     len(fullresult)))
                return fullresult


    @backoff(0.2, 2, 10)
    def _pg_execute_one(self, query):
        with psycopg2.connect(**self.dsn, cursor_factory=RealDictCursor) as self._connection:
            with self._connection.cursor() as self._cursor:
                self._cursor.execute(query)
                return self._cursor.fetchone()

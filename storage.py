from abc import ABC, abstractmethod
from os.path import isfile
import sqlite3


class Storage(ABC):
    
    @abstractmethod
    def save(self, data: str) -> None:
        assert False
    
    @abstractmethod
    def retrieve(self, id: int) -> str:
        assert False


class DatabaseStorage(Storage):
    __db_name: str

    def __init__(self, db_name: str) -> None:
        self.__db_name = db_name
        if isfile(self.__db_name):
            return
        self._init_db()
    
    def save(self, data: str) -> None:
        connection = sqlite3.connect(self.__db_name)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Data (value)
            VALUES (?)
        ''', (data,))
        connection.commit()
        connection.close()
    
    def retrieve(self, id: int) -> str:
        connection = sqlite3.connect(self.__db_name)
        cursor = connection.cursor()
        cursor.execute('''
            SELECT value FROM Data
            WHERE id = ?
        ''', (id + 1,))
        result = cursor.fetchone()
        connection.close()
        return result[0]
    
    
    def _init_db(self):
        connection = sqlite3.connect(self.__db_name)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE Data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()


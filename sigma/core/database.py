import sqlite3

from .logger import create_logger


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class Database(object):
    def __init__(self, dbpath=None):
        self.db = None
        self.log = create_logger('database')

        if dbpath:
            self.connect(dbpath)

    def connect(self, dbpath, timeout=20):
        self.db = sqlite3.connect(dbpath, timeout=timeout)

    def execute(self, sql, *args):
        results = None

        if self.db:
            try:
                results = self.db.execute(sql, args)
            except sqlite3.IntegrityError as e:
                self.log.error(e)
                raise IntegrityError
            except sqlite3.DatabaseError as e:
                self.log.error(e)
                raise DatabaseError

        return results

    def rollback(self):
        if self.db:
            self.db.rollback()

    def commit(self):
        if self.db:
            self.db.commit()

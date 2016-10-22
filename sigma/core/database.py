import os
import sqlite3

from .logger import create_logger


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class Database(object):
    def __init__(self, dbpath, sql_file=None):
        self.db = None
        self.log = create_logger('database')

        if dbpath:
            self.connect(dbpath)
        else:
            raise DatabaseError('No database file given!')

        # perform db init
        if sql_file:
            if os.path.exists(sql_file):
                sql_script = open(sql_file).read()
                self.db.executescript(sql_script)
                self.commit()
            else:
                msg = 'SQL file {:s} does not exist!'
                raise DatabaseError(msg.format(sql_file))

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

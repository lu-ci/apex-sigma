import os
import pymongo

from .logger import create_logger


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class Database(object):
    def __init__(self, db_addr):
        self.db = None
        self.log = create_logger('database')

        if db_addr:
            self.connect(db_addr)
        else:
            raise DatabaseError('No database address given!')


    def connect(self, db_addr):
        self.moncli = pymongo.MongoClient(db_addr)
        self.db = self.moncli.aurora

    def insert_one(self, collection, data):
        if self.db:
            self.db[collection].insert_one(data)

    def find(self, collection, data):
        if self.db:
            result = self.db[collection].find(data)
            return result

    def update_one(self, collection, data):
        if self.db:
            self.db[collection].update_one(data)

    def delete_one(self, collection, data):
        if self.db:
            self.db[collection].delete_one(data)

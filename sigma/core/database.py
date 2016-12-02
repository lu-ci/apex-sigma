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

    def update_one(self, collection, target, data):
        if self.db:
            self.db[collection].update_one(target, data)

    def delete_one(self, collection, data):
        if self.db:
            self.db[collection].delete_one(data)

    def add_stats(self, statname):
        if self.db:
            collection = 'Stats'
            find_data = {
                'Role': 'Stats'
            }
            find_res = self.db[collection].find(find_data)
            count = 0
            for res in find_res:
                try:
                    count = res[statname]
                except:
                    count = 0
            new_count = count + 1
            updatetarget = {"Role": 'Stats'}
            updatedata = {"$set": {statname: new_count}}
            self.db[collection].update_one(updatetarget, updatedata)

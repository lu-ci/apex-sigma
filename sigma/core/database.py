import pymongo

from .logger import create_logger
from .db_nodes.stats import add_stats_node, update_population_stats_node, init_stats_table_node
from .db_nodes.points import point_manipulation, point_grabber
from .db_nodes.refactor import refactor_servers_node, refactor_users_node
from .db_nodes.details import update_details
from .db_nodes.settings import set_settings_node, add_new_server_settings_node
from .db_nodes.settings import get_settings_node, init_server_settings_node, check_for_missing_settings_node
from .db_nodes.inventory import get_inventory, add_to_inventory, del_from_inventory


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class Database(object):
    def __init__(self, db_addr, port, auth, unam, pwd):
        self.db = None
        self.log = create_logger('Database')

        if db_addr:
            self.connect(db_addr, port, auth, unam, pwd)
        else:
            raise DatabaseError('No database address given!')

    def connect(self, db_addr, port, auth, unam, pwd):
        if not auth:
            self.moncli = pymongo.MongoClient(db_addr)
        else:
            mongo_address = 'mongodb://{:s}:{:s}@{:s}:{:s}/'.format(unam, pwd, db_addr, str(port))
            self.moncli = pymongo.MongoClient(mongo_address)
        self.db = self.moncli.aurora
        self.db.log = self.log

    # Core Control Nodes
    def insert_one(self, collection, data):
        self.db[collection].insert_one(data)

    def find(self, collection, data):
        result = self.db[collection].find(data)
        return result

    def find_one(self, collection, data):
        result = self.db[collection].find_one(data)
        return result

    def update_one(self, collection, target, data):
        self.db[collection].update_one(target, data)

    def delete_one(self, collection, data):
        self.db[collection].delete_one(data)

    # Side Control Nodes
    def init_stats_table(self):
        init_stats_table_node(self.db)

    def add_stats(self, statname):
        add_stats_node(self.db, statname)

    def update_population_stats(self, servers, members):
        update_population_stats_node(self.db, servers, members)

    def add_points(self, server, user, points):
        point_manipulation(self.db, server, user, points, True)

    def take_points(self, server, user, points):
        point_manipulation(self.db, server, user, points, False)

    def get_points(self, user):
        return point_grabber(self.db, user)

    def get_inv(self, user):
        return get_inventory(self.db, user)

    def inv_add(self, user, item):
        add_to_inventory(self.db, user, item)

    def inv_del(self, user, item_id):
        del_from_inventory(self.db, user, item_id)

    async def refactor_users(self, usrgen):
        await refactor_users_node(self.db, usrgen)

    async def refactor_servers(self, servers):
        await refactor_servers_node(self.db, servers)

    def update_server_details(self, server):
        update_details(self.db, server=server)

    def update_user_details(self, user):
        update_details(self.db, user=user)

    def add_new_server_settings(self, server):
        add_new_server_settings_node(self.db, server)

    def init_server_settings(self, servers):
        init_server_settings_node(self.db, servers)

    def get_settings(self, server_id, setting):
        return get_settings_node(self.db, server_id, setting)

    def set_settings(self, server_id, setting, setting_variable):
        set_settings_node(self.db, server_id, setting, setting_variable)

    def check_for_missing_settings(self, server):
        check_for_missing_settings_node(self.db, server)


import pymongo

from .logger import create_logger
from .db_nodes.cooldown import get_cooldown_node, on_cooldown_node, set_cooldown_node
from .db_nodes.stats import add_stats_node, update_population_stats_node, init_stats_table_node
from .db_nodes.points import add_points_node, get_points_node, take_points_node
from .db_nodes.refactor import refactor_servers_node, refactor_users_node
from .db_nodes.details import update_server_details_node, update_user_details_node
from .db_nodes.settings import set_settings_node, add_new_server_settings_node
from .db_nodes.settings import get_settings_node, init_server_settings_node


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class Database(object):
    def __init__(self, db_addr, port, auth, unam, pwd):
        self.db = None
        self.log = create_logger('database')

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

    def set_cooldown(self, sid, uid, command):
        set_cooldown_node(self.db, sid, uid, command)

    def on_cooldown(self, sid, uid, command, cooldown):
        on_cooldown_node(self.db, sid, uid, command, cooldown)

    def get_cooldown(self, sid, uid, command, cooldown):
        get_cooldown_node(self.db, sid, uid, command, cooldown)

    def add_points(self, server, user, points):
        add_points_node(self.db, server, user, points)

    def take_points(self, server, user, points):
        take_points_node(self.db, server, user, points)

    def get_points(self, server, user):
        get_points_node(self.db, server, user)

    def refactor_users(self, usrgen):
        refactor_users_node(self.db, usrgen)

    def refactor_servers(self, servers):
        refactor_servers_node(self.db, servers)

    def update_server_details(self, server):
        update_server_details_node(self.db, server)

    def update_user_details(self, user):
        update_user_details_node(self.db, user)

    def add_new_server_settings(self, server):
        add_new_server_settings_node(self.db, server)

    def init_server_settings(self, servers):
        init_server_settings_node(self.db, servers)

    def get_settings(self, server_id, setting):
        get_settings_node(self.db, server_id, setting)

    def set_settings(self, server_id, setting, setting_variable):
        set_settings_node(self.db, server_id, setting, setting_variable)

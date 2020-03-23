import pymongo
from bson.json_util import dumps


DB = "db"
USERS_COL = "users"
SNAPSHOT_COL = "snapshots"
DATA_COL = "data"


class MongoDB:
    prefix = 'mongodb'

    def __init__(self, host, port):
        self.address = f'{host}:{port}'
        self.client = pymongo.MongoClient(f'mongodb://{self.address}')  # TODO: change paramter to host, port?
        self.db = self.client[DB]
        self.users = self.db[USERS_COL]
        self.snapshots = self.db[SNAPSHOT_COL]
        self.data = self.db[DATA_COL]

    def __repr__(self):
        return f'MongoDB({self.address})'

    def insert_user(self, user):
        self.users.insert_one(user)

    def insert_data(self, topic, data):
        if type(data) == dict:
            self.snapshots.insert_one({'topic': topic, **data})

        if type(data) == str:
            self.snapshots.insert_one({'topic': topic, 'data': data})

    def get_users(self):
        return dumps(self.users.find())

    def get_user_by_id(self, user_id):
        return dumps(self.users.find_one({'user_id': user_id}))

    def get_data_by_user_id(self, user_id):
        return dumps(self.snapshots.find({'user_id': user_id}))

    def get_data_by_user_snapshot_id(self, user_id, snapshot_id):
        return dumps(self.snapshots.find({'user_id': user_id}, {'snapshot_id': snapshot_id}))

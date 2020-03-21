import pymongo
# docker run -d mongo
# docker run -d -p 27017:27017 -v ~/data:/data/db mongo
# docker run -d -p 27017:27017 mongo

DB = "db"
USERS_COL = "users"
SNAPSHOT_COL = "snapshots"
DATA_COL = "data"


class MongoDB:
    prefix = 'mongodb'

    def __init__(self, host, port):
        self.address = f'{host}:{port}'
        self.client = pymongo.MongoClient(f'mongodb://{self.address}')
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
            self.snapshots.insert_one({'name': topic, 'data': data})

    def get_users(self):
        return self.users.find()

    def get_user_by_id(self, user_id):
        return self.users.find({'id': user_id})

    def get_data_by_user_id(self, user_id):
        return self.snapshots.find({'user_id': user_id})

    def get_data_by_user_snapshot_id(self, user_id, snapshot_id):
        return self.snapshots.find({'user_id': user_id}, {'snapshot_id': snapshot_id})

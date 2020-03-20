import pymongo
# docker run -d mongo
# docker run -d -p 27017:27017 -v ~/data:/data/db mongo


DB = "db"  # we use a single DB
USERS_COL = "users"
SNAPSHOT_COL = "snapshots"
DATA_COL = "data"

class MongoDB:
    def __init__(self, host):
        self.client = pymongo.MongoClient(f'mongodb://{host}')
        self.db = self.client[DB]
        self.users = self.db[USERS_COL]
        self.snapshots = self.db[SNAPSHOT_COL]
        self.data = self.db[DATA_COL]

    def create_collection(self, collection_name): # collection is created on demand
        pass

    def insert_user(self, user):
        self.users.insert_one({'id': user.user_id, 'name': user.username, 'birthday': user.birthday, 'gender': user.gender})

    def insert_snapshot(self, user):
        pass

    def insert_data(self, snapshot_id, user_id, topic, data):
        if type(data) == dict:
            self.snapshots.insert_one({'snapshot_id': snapshot_id, 'user_id': user_id, 'topic': topic, **data})
        if type(data) == str:
            self.snapshots.insert_one({'snapshot_id': snapshot_id, 'user_id': user_id, 'name': topic, 'data': data})

    def get_users(self):
        return self.users.find()

    def get_user_by_id(self, user_id):
        return self.users.find({'id': user_id})

    def get_data_by_user_id(self, user_id):
        return self.snapshots.find({'user_id': user_id})

    def get_data_by_user_snapshot_id(self, user_id, snapshot_id):
        return self.snapshots.find({'user_id': user_id}, {'snapshot_id': snapshot_id})

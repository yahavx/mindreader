import pymongo

from mindreader.objects import User

DB = "db"
USERS_COL = "users"
SNAPSHOT_COL = "snapshots"


class MongoDB:
    prefix = 'mongodb'

    def __init__(self, host: str, port: int):
        """
        Connects to the mongo db client. Timeouts after 2 minutes.

        :param host: client host.
        :param port: client port.
        """
        self.host = host
        self.port = port
        try:
            self.client = pymongo.MongoClient(host, int(port), serverSelectionTimeoutMS=120000)
        except pymongo.errors.ServerSelectionTimeoutError:
            raise ConnectionError

        self.db = self.client[DB]
        self.users = self.db[USERS_COL]
        self.snapshots = self.db[SNAPSHOT_COL]

        try:  # check the connection
            self.client.server_info()  # the connection is not a must right now, but better to detect errors now
        except pymongo.errors.ServerSelectionTimeoutError:
            raise ConnectionError

    def __repr__(self):
        return f'MongoDB({self.host}:{self.port})'

    def insert_user(self, user: User):
        user_dict = dict(username=user.username, user_id=user.user_id, birthday=user.birthday, gender=user.gender)
        self.users.update_one({'user_id': user.user_id}, {'$set': user_dict}, upsert=True)

    def insert_data(self, data):
        snapshot_id = data['metadata']['snapshot_id']
        user_id = data['metadata']['user_id']
        timestamp = data['metadata']['timestamp']
        self.snapshots.update_one({'metadata':
                                       {'snapshot_id': snapshot_id, 'user_id': user_id, 'timestamp': timestamp}},
                                  [{'$set': data}], upsert=True)  # create or update

    def get_users(self):
        return list(self.users.find({}, {'_id': 0}))

    def get_user_by_id(self, user_id):
        return self.users.find_one({'user_id': user_id}, {'_id': 0})

    def get_snapshots_by_user_id(self, user_id):
        return list(self.snapshots.find({'user_id': user_id}, {'_id': 0}))

    def get_snapshot_by_id(self, user_id, snapshot_id):
        return self.snapshots.find_one({'user_id': user_id, 'snapshot_id': snapshot_id}, {'_id': 0})

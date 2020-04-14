import importlib
import sys
from furl import furl
from pathlib import Path


supported_dbs = {}


class Database:
    def __init__(self, url):
        url = furl(url)
        prefix = url.scheme
        if prefix not in supported_dbs:
            raise NotImplementedError(f"Database type ('{prefix}') is not supported")
        try:
            self.db = supported_dbs[prefix](url.host, url.port)
        except ConnectionError:
            raise ConnectionError("Couldn't connect to database")

    def __repr__(self):
        return self.db.__repr__()

    def insert_user(self, user):
        self.db.insert_user(user)

    def insert_data(self, data):
        self.db.insert_data(data)

    def get_users(self):
        return self.db.get_users()

    def get_user_by_id(self, user_id):
        return self.db.get_user_by_id(user_id)

    def get_snapshots_by_user_id(self, user_id):
        return self.db.get_snapshots_by_user_id(user_id)

    def get_snapshot_by_id(self, user_id, snapshot_id):
        return self.db.get_snapshot_by_id(user_id, snapshot_id)


def load_databases():
    root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or file.name == 'database.py' or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, db in module.__dict__.items():
            if isinstance(db, type) and db.__name__.endswith("DB"):
                supported_dbs[db.prefix] = db


load_databases()

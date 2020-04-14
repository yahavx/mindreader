import importlib
import sys
from furl import furl
from pathlib import Path

from mindreader.objects import User

supported_dbs = {}


class Database:
    """
    This class is used to communicate with databases.
    It is called databases but in fact its a thick layer above it (sometimes called persistence).

    Note that all the functions that query the database can return empty objects.
    It's the users responsibility to handle that if necessary.

    To add a new database, add a file named <name>db.py to this package,
    with a class named <name>DB, which has an attribute named 'prefix' (string),
    which is the database name. It should implement the functions below.
    """
    def __init__(self, url):
        """
        Initializes a new database.

        :param url: url of the database, with the prefix indicating the database type.

        :raises NotImplementedError: the database type is not supported.
        :raises ConnectionError: connection couldn't be established in less than two minutes.
        """
        url = furl(url)
        prefix = url.scheme
        if prefix not in supported_dbs:
            raise NotImplementedError(f"Database type ('{prefix}') is not supported")
        try:
            self.db = supported_dbs[prefix](url.host, url.port)
        except ConnectionError:
            raise ConnectionError(f"Couldn't connect to '{prefix}' database")

    def __repr__(self):
        """Returns a compact representation of the database client."""
        return self.db.__repr__()

    def insert_user(self, user: User):
        """
        Inserts a user to the database.
        If user with the same id already exists, it will update his entry.
        """
        self.db.insert_user(user)

    def insert_data(self, data: dict):
        """
        Inserts data to the database.
        The data should be a dictionary,
        and contain a 'metadata' entry (that is similar to objects/SnapshotMetadata class).
        """
        self.db.insert_data(data)

    def get_users(self) -> list:
        """Returns the list of available users."""
        return self.db.get_users()

    def get_user_by_id(self, user_id) -> dict:
        """Returns a user that matches the user_id."""
        return self.db.get_user_by_id(user_id)

    def get_snapshots_by_user_id(self, user_id) -> list:
        """Returns list of snapshots (metadata) that belongs to user with user_id."""
        return self.db.get_snapshots_by_user_id(user_id)

    def get_snapshot_by_id(self, user_id, snapshot_id) -> dict:
        """Returns a snapshot with snapshot_id (metadata, and available topics)."""
        return self.db.get_snapshot_by_id(user_id, snapshot_id)


def load_databases():
    """Loads dynamically all the available databases."""
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

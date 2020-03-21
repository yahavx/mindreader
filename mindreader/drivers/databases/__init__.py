import importlib
import sys
from furl import furl
from pathlib import Path

config = {}


def load_databases():
    root = Path("mindreader/drivers/databases").absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, db in module.__dict__.items():
            if isinstance(db, type) and db.__name__.endswith("DB"):
                config[db.prefix] = db


def init_database(url):
    url = furl(url)
    prefix = url.scheme
    if prefix not in config:
        raise ValueError("Database type is not supported")
    return config[prefix](url.host, url.port)


load_databases()

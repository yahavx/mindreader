import importlib
import sys
from furl import furl
from pathlib import Path

config = {}


def load_message_queues():
    root = Path("mindreader/drivers/message_queues").absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, mq in module.__dict__.items():
            if isinstance(mq, type) and mq.__name__.endswith("MQ"):
                config[mq.name] = mq


def init_queue(url):
    url = furl(url)
    prefix = url.scheme
    if prefix not in config:
        raise ValueError("Message queue type is not supported")
    return config[prefix](url.host, url.port)


load_message_queues()

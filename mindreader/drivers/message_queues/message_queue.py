import importlib
import sys
from furl import furl
from pathlib import Path


supported_mqs = {}


class MessageQueue:
    def __init__(self, url):
        url = furl(url)
        prefix = url.scheme
        if prefix not in supported_mqs:
            raise NotImplementedError(f"Message queue type ('{prefix}') is not supported")
        try:
            self.mq = supported_mqs[prefix](url.host, url.port)
        except ConnectionError:
            raise ConnectionError("Couldn't connect to message queue")

    def __repr__(self):
        return self.mq.__repr__()

    def publish(self, topic, message):
        self.mq.publish(topic, message)

    def consume(self, topic, handler, queue=''):
        self.mq.consume(topic, handler, queue)


def load_message_queues():
    root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, mq in module.__dict__.items():
            if isinstance(mq, type) and mq.__name__.endswith("MQ"):
                supported_mqs[mq.prefix] = mq


load_message_queues()

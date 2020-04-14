import importlib
import sys
from furl import furl
from pathlib import Path

supported_mqs = {}
"""
Mapping of the supported message queses, loaded dynamically.
Currently available:
RabbitMQ - 'rabbitmq'
"""


class MessageQueue:
    """
    A message queue that allows sending and consuming messages.

    To add a new message queue, add a file named <name>_mq.py to the current-package,
    with a class named <name>MQ, which has an attribute named 'prefix' (string),
    which is the message queue name. It should implement the functions below.
    Make sure you update the prefix you chose in 'supported_dbs' above.
    """

    def __init__(self, url):
        """
        Initializes a new message queue.

        :param url: url of the message queue, with the prefix indicating the message queue type.

        :raises NotImplementedError: the message queue type is not supported.
        :raises ConnectionError: connection couldn't be established in less than two minutes.
        """
        url = furl(url)
        prefix = url.scheme
        if prefix not in supported_mqs:
            raise NotImplementedError(f"Message queue type ('{prefix}') is not supported")
        try:
            self.mq = supported_mqs[prefix](url.host, url.port)
        except ConnectionError:
            raise ConnectionError(f"Couldn't connect to '{prefix}' message queue")

    def __repr__(self):
        """Returns a compact representation of the message queue client."""
        return self.mq.__repr__()

    def publish(self, topic, message):
        """
        Publishes a message to the queue.

        :param topic: the name of the exchange to post into (consumers will have to use that to receive messages).
        :param message: the data, encoded in JSON format.
        """
        self.mq.publish(topic, message)

    def consume(self, topic, handler, queue=''):
        """
        Listens to an exchange, and handle messages received.
        Note that this function is blocking.

        :param topic: the name of the exchange to subscribe to.
        :param handler: a function that receives
        :param queue: optional parameter, allows multiple consumers to split the load between them.
                      if not supported, a unique queue is generated.
        :return:
        """
        self.mq.consume(topic, handler, queue)


def load_message_queues():
    """Loads dynamically all the available message queues."""
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

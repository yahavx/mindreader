import json
from threading import Thread

from mindreader.drivers import Database, MessageQueue, Encoder
from mindreader.parsers import get_available_parsers


class Saver:
    def __init__(self, database_url):
        self.db = Database(database_url)

    def save(self, topic: str, data: str, debug: bool = False):
        """
        Saves data to the database.

        :param topic: The type of the data (user, pose, etc).
        :param data: The data, in JSON format.
        :param debug: if enabled, the data will be printed before saved to the database.
        :return:
        """
        if debug:
            print(f'Saving data of type {topic}')
            print(data)

        if topic == 'user':
            encoder = Encoder('json')
            user = encoder.user_decode(data)
            self.db.insert_user(user)
        else:
            data = json.loads(data)
            self.db.insert_data(data)

    def run_saver(self, topic: str, mq: MessageQueue, debug=False):
        """
        Registers to a message queue on a single parser type,
        received snapshot parsing results, and saves them to the database.

        :param topic: The type of parsed data it consumes (user, pose, etc).
        :param mq: A message queue. Note that it should already be initialized (not a url).
        :param debug: if enabled, each data will be printed before saved to the database.
        """
        mq.consume(topic, lambda data: self.save(topic, data, debug))

    def run_all_savers(self, mq_url: str, debug: bool = False):
        """
        Runs the saver as a service, so it listens on the queue, and saves the data received to the database.

        :param mq_url: Receives a url to a message queue, and consumes data from all available parsers.
        :param debug:  if enabled, each data will be printed before saved to the database.
        """

        mq = MessageQueue(mq_url)
        print("Saver connected to the queue")
        for parser_name in [*get_available_parsers(), 'user']:
            t = Thread(target=self.run_saver, args=(parser_name, mq, debug))
            t.start()

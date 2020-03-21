import json
from ..drivers.databases import init_database
from ..drivers.message_queues import init_queue


class Saver:
    def __init__(self, database_url):
        self.db = init_database(database_url)

    def save(self, topic, data):
        data = json.loads(data)
        if topic == 'user':
            self.db.insert_user(data)
        else:
            self.db.insert_data(topic, data)

    def run_saver(self, mq_url):
        mq = init_queue(mq_url)
        pass

    def collect_topics(self):
        pass




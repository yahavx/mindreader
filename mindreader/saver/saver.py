import json
from ..drivers.databases import init_database
from ..drivers.message_queues import init_queue
from ..parsers import get_available_parsers


class Saver:
    def __init__(self, database_url):
        self.db = init_database(database_url)

    def save(self, topic, data):
        print(f'Now saving {topic}')
        data = json.loads(data)
        if topic == 'user':
            self.db.insert_user(data)
        else:
            self.db.insert_data(topic, data)

    def run_saver(self, mq_url):
        mq = init_queue(mq_url)

        for parser_name in get_available_parsers():
            if parser_name != 'rotation':
                continue
            print(f'Now listening on exchange: {parser_name}')
            mq.consume(parser_name, lambda body: self.save(parser_name, body))




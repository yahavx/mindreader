import pika
import importlib
import sys
from mindreader.utils.encoder.pb_encoder import PBEncoder
from pathlib import Path

# docker run -d -p 5672:5672 rabbitmq

config = {}


def parse(parser_name, data):
    return config[parser_name](data)


def run_all_parsers(context, snapshot):
    for parser in config.values():
        parser(context, snapshot)


def consume(handler='', name=''):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshot', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='snapshot', queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print('Waiting for messages')
    channel.start_consuming()


def load_parsers():
    root = Path("mindreader/parsers").absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)
        for key, func in module.__dict__.items():
            if callable(func) and func.__name__.startswith("parse"):
                config[func.field] = func


def callback(channel, method, properties, body):
    user, snapshot = PBEncoder.message_decode(body)
    print(user)
    print(f'snapshot time: {snapshot.datetime}')

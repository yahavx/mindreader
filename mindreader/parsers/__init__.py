import importlib
import json
import sys
from pathlib import Path
from mindreader.drivers.message_queues import init_queue

config = {}


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


def parse(parser_name, raw_data):
    return config[parser_name](raw_data)


def run_parser(parser_name, mq_url):
    mq = init_queue(mq_url)

    def handler(body):
        result = parse(parser_name, body)
        print(result)
        mq.publish(parser_name, result)

    mq.consume('snapshot', handler)


def run_all_parsers(mq_url):
    for parser in config.keys():
        run_parser(parser, mq_url)


def get_available_parsers():
    return list(config.keys())


load_parsers()

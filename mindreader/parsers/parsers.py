import sys
import importlib
import json
from pathlib import Path
from threading import Thread

from mindreader.drivers import MessageQueue


available_parsers = {}


def parse(parser_name: str, raw_snapshot: str):
    """
    Runs a parser on a snapshot.

    :param parser_name: name of the parser to use.
    :param raw_snapshot: a snapshot, in raw (JSON) format.

    :raises NotImplementedError: the parser does not exist.

    :return: the result of the parsing, in JSON format.
    """
    if parser_name not in available_parsers:
        raise NotImplementedError("Parser type is not supported")

    parser = available_parsers[parser_name]
    return parser(raw_snapshot)


def run_parser(parser_name: str, mq_url: str):
    """
    Runs a parser as a service, so it registers to a message queue,
    parse snapshots received on a queue, and pass the results back to another queue.

    :param parser_name: name of the parser to use.
    :param mq_url: a url to the queue. The prefix should indicate the type of the message queue
    (for example: rabbitmq://...)
    """
    mq = MessageQueue(mq_url)
    print(f"Parser {parser_name} connected to the queue")

    def handler(snapshot):
        result = parse(parser_name, snapshot)
        wrapped = wrap_parser_result(parser_name, result, snapshot)
        print(f"Parsed {parser_name}")
        mq.publish(parser_name, wrapped)

    mq.consume('snapshot', handler)


def wrap_parser_result(data_type, data, snapshot):
    """
    Wraps data produced by a parser, with metadata needed for the next stages.

    :param data_type: The type of the data (usually the name of the parser that produced it).
    :param data: The data, produced by some parser, in JSON format.
    :param snapshot: A snapshot, in JSON format.

    :return: The wrapped object, in JSON format.
    """
    snapshot = json.loads(snapshot)
    data = json.loads(data)
    wrapped = {'snapshot_id': snapshot['snapshot_id'],
               'results': {data_type: data}}
    return json.dumps(wrapped)


def run_all_parsers(mq_url):
    """
    Receives a url to a message queue, and runs all parsers available, each in a different thread (using run_parser).
    """
    for parser_name in get_available_parsers():
        t = Thread(target=run_parser, args=(parser_name, mq_url))
        t.start()


def get_available_parsers():
    """Returns the list of available parsers."""
    return list(available_parsers.keys())


def load_parsers():
    """
    Loads dynamically all the available parsers.
    In order to add a new parser, check the 'parsers' section in the README of the project.
    """
    root = Path("mindreader/parsers").absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or file.name == 'parsers.py' or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)
        for key, func in module.__dict__.items():
            if callable(func) and func.__name__.startswith("parse"):
                available_parsers[func.field] = func


load_parsers()

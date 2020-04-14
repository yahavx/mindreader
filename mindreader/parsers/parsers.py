import sys
import importlib
import json
from pathlib import Path
from threading import Thread

from mindreader.drivers import MessageQueue, Encoder
from mindreader.objects import Snapshot

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

    encoder = Encoder('json')
    snapshot = encoder.snapshot_decode(raw_snapshot)

    parsing_result = parser(snapshot)
    wrapped_parsing_result = wrap_parser_result(parsing_result, parser_name, snapshot)  # wrap with metadata
    ret = json.dumps(wrapped_parsing_result, indent=4)
    return ret


def run_parser(parser_name: str, mq_url: str, debug: bool = False):
    """
    Runs a parser as a service, so it registers to a message queue,
    parse snapshots received on a queue, and pass the results back to another queue.

    :param parser_name: name of the parser to use.
    :param mq_url: a url to the queue. The prefix should indicate the type of the message queue
                   (for example: rabbitmq://...)
    :param debug: if enabled, the parsing results will be printed before passing them to the queue
    """
    mq = MessageQueue(mq_url)
    print(f"Parser {parser_name} connected to the queue")

    def handler(snapshot):
        result = parse(parser_name, snapshot)
        if debug:
            print("Parsed a snapshot:")
            print(result)
        mq.publish(parser_name, result)

    mq.consume('snapshot', handler, queue=parser_name)


def wrap_parser_result(data: dict, data_type: str, snapshot: Snapshot) -> dict:
    """
    Wraps data produced by a parser, with metadata needed for the next stages.

    :param data: The data, produced by some parser
    :param data_type: The type of the data (usually the name of the parser that produced it).
    :param snapshot: A snapshot object

    :return: The wrapped object
    """
    metadata = dict(timestamp=snapshot.metadata.timestamp, user_id=snapshot.metadata.user_id,
                    snapshot_id=snapshot.metadata.snapshot_id)
    return {'metadata': metadata, data_type: data}


def run_all_parsers(mq_url):
    """
    Receives a url to a message queue, and runs all parsers available, each in a different thread (using run_parser).
    """
    for parser_name in get_available_parsers():
        t = Thread(target=run_parser, args=(parser_name, mq_url))
        t.start()


def get_available_parsers() -> list:
    """Returns the list of available parsers."""
    return list(available_parsers.keys())


def load_parsers():
    """
    Loads dynamically all the available parsers.
    In order to add a new parser, check the 'parsers' section in the README.md of this package.
    """
    root = (Path(__file__).parent / 'parser_workers').absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or file.name == 'parsers.py' or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)
        for key, func in module.__dict__.items():
            if callable(func) and func.__name__.startswith("parse"):
                available_parsers[func.field] = func


load_parsers()

import importlib
import sys
from pathlib import Path

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


def run_all_parsers(context, snapshot):
    for parser in config.values():
        parser(context, snapshot)


load_parsers()

import importlib
import json
from pathlib import Path
import datetime as dt
import sys
from .client import snap_decode, user_decode
from flask import Flask, make_response, jsonify, request
import os

serv = Flask(__name__)
data_dir = None
config = {}


def run_server(address, data_dirr):
    global data_dir
    data_dir = Path(data_dirr).absolute()
    load_parsers()
    serv.run(*address)




@serv.route('/config', methods=['GET'])
def get_config():
    return json.dumps(list(config.keys()))


@serv.route('/snapshot', methods=['POST'])
def post_snapshot():
    user_json, snapshot_json = request.get_json(force=True)
    user = user_decode(user_json)
    snapshot = snap_decode(snapshot_json)

    context = Context.generate_context(user, snapshot)
    parse(context, snapshot)
    print("Finished!")
    return ""


def parse(context, snapshot):
    for parser in config.values():
        parser(context, snapshot)


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


class Context:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def save(self, name, data):
        with open(self.path(name), 'w') as f:
            f.write(data)

    def path(self, name):
        return str(self.data_dir / name)

    @classmethod
    def generate_context(cls, user, snapshot):
        date = dt.datetime.fromtimestamp(snapshot.timestamp / 1000).strftime('%Y-%m-%d_%H-%M-%S-%f')
        return Context(data_dir / str(user.user_id) / date)



import json
import os


data_dir = '/var/data/mindreader_data'
# this path is configured to allow the containers to communicate, so changes should be considered carefully


class Context:
    def __init__(self, user_id: int, snapshot_id: str):
        self.data_dir = f'{data_dir}/{user_id}/{snapshot_id}'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save(self, name, data):
        path = self.path(name)
        mode = 'wb+' if type(data) == bytes else 'w+'
        with open(path, mode) as f:
            f.write(data)
        return path

    def load(self, name, byte=False):
        path = self.path(name)
        mode = 'rb' if byte else 'r'
        with open(path, mode) as f:
            return f.read()

    def path(self, name):
        return f'{self.data_dir}/{name}'

    @classmethod
    def generate_from_snapshot(cls, snapshot):
        return cls(snapshot["user_id"], snapshot["snapshot_id"])

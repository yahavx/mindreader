import json
import os


class Context:  # this class is used to work with the disk
    def __init__(self, data_dir, user_id, snapshot_id):
        self.data_dir = f'{data_dir}/{user_id}/{snapshot_id}'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save(self, name, data):
        path = self.path(name)
        mode = 'wb+' if type(data) == bytes else 'w+'
        with open(path, mode) as f:
            f.write(data)
        return path

    # def load_bytes(self, name):
    #     path = self.path(name)
    #     with open(path, 'rb') as f:
    #         return f.read()

    def load(self, name):
        path = self.path(name)
        with open(path, 'r') as f:
            return f.read()

    def path(self, name):
        return f'{self.data_dir}/{name}'

    @classmethod
    def generate_from_snapshot(cls, data_dir, snapshot):
        return cls(data_dir, snapshot["user_id"], snapshot["snapshot_id"])

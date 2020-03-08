import datetime as dt
import os


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
        # return Context(data_dir / str(user.user_id) / date)
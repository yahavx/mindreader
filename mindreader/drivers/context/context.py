import json
import os
from pathlib import Path

from mindreader.objects.snapshot_utils import SnapshotMetadata


class Context:
    """
    This class is used to communicate with the storage (i.e. save/load files).
    """

    base_dir = '~/mindreader_internal_data'

    def __init__(self, path: str, is_file=False):
        """
        Generate context from a path.
        It is recommended that the resulting absolute path will start with base_dir.

        :param path: the context base path. Should be a directory, but may not exist (auto-created).
        :param is_file: should be True if the path supplied is to a file (not to a directory).
                        In that case, the directory of the file will be evaluated
        """
        path = Path(path)
        if is_file:
            path = path.parent
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    @classmethod
    def generate_context_from_snapshot_metadata(cls, metadata: SnapshotMetadata):
        """Generate a context that is based on snapshot metadata."""
        return cls(f'{cls.base_dir}/{metadata.user_id}/{metadata.snapshot_id}')

    def save(self, name: str, data, is_json=False):
        """
        Saves data to storage.

        :param name: name of the saved file.
        :param data: the data to save. should be in a format that can be saved.
        :param is_json: should be True if data is in JSON format (not already dumped).
        """
        path = self.get_file_path(name)
        mode = 'wb+' if type(data) == bytes else 'w+'

        if is_json:
            data = json.dumps(data)

        with open(path, mode) as f:
            f.write(data)

        return path

    def load(self, name, byte=False, is_json=False):
        """
        Loads file from storage.

        :param name: name of the file, in the context directory.
        :param byte: should be set to True if the data to be loaded is in bytes format.
        :param is_json: should be set to True if the data to be loaded is in JSON format.
        """
        path = self.get_file_path(name)
        mode = 'rb' if byte else 'r'

        with open(path, mode) as f:
            res = f.read()

        if is_json:
            return json.loads(res)
        return res

    def get_file_path(self, name):
        """
        Return the full path of a file in the context directory.
        Its on the caller responsibility to validate the existence of the path/file if needed.

        :param name: name of the file, in the context directory.
        """
        return f'{self.path}/{name}'

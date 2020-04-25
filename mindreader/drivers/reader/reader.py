import importlib
import sys
from pathlib import Path
from mindreader.objects import Snapshot, User


supported_file_readers = {}
"""
Mapping of the supported file formats, loaded dynamically.
Currently available:
Protobuf - 'protobuf'
"""


class Reader:
    """
    This class is used to reads users and snapshots from files.
    It serves as an interface to the available readers.

    To add a new reader, add a file named <name>_file_reader.py to the sub-package file_readers
    with a class named <name>FileReader, which has an attribute named 'prefix' (string),
    that indicates the type of files it supports reading from. It should implement the functions below.
    Make sure you update the prefix you chose in 'supported_dbs' above.
    """

    def __init__(self, path: str, file_format: str):
        """
        Initializes a new reader.

        :param path: path to the file.
        :param file_format: format of the file.

        :raises NotImplementedError: the format type received is currently not supported.
        """
        if file_format not in supported_file_readers:
            raise NotImplementedError("File format is not supported")
        self.file_reader = supported_file_readers[file_format]()
        self.file_reader.open_file(path)
        self.user = self.file_reader.get_user()

    def get_user(self) -> User:
        """Returns the user associated to the file."""
        return self.user

    def get_snapshot(self) -> Snapshot:
        """Returns the next snapshot in the file."""
        return self.file_reader.get_snapshot()

    def __repr__(self):
        path = self.path
        return f'Reader({path=}, user={self.user.username})'

    def __str__(self):
        return f'Reader(path={self.path}, user={self.user.username})'

    def __iter__(self):
        """Iterates over all the snapshots in the file."""
        snapshot = self.file_reader.get_snapshot()
        while snapshot:
            yield snapshot
            snapshot = self.file_reader.get_snapshot()

    def close(self):
        self.file_reader.stream.close()


def load_readers():
    """Loads dynamically all the available file readers."""
    root = (Path(__file__).parent / 'file_readers').absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, filereader in module.__dict__.items():
            if isinstance(filereader, type) and filereader.__name__.endswith("Reader"):
                supported_file_readers[filereader.prefix] = filereader


load_readers()

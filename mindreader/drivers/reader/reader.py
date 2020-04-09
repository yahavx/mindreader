from pathlib import Path
import importlib
import sys


supported_file_readers = {}
"""Holds the list of supported file formats, loaded dynamically."""


class Reader:
    """This class is used to parse users and snapshots from files."""

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
        self.user = self.file_reader.get_user_information()

    def get_user(self):
        """Returns the user associated to the file."""
        return self.user

    def get_snapshot(self):
        """Returns the next snapshot in the file."""
        return self.file_reader.get_snapshot()

    def __repr__(self):
        path = self.path
        return f'Reader({path=}, user={self.user.username})'

    def __str__(self):
        path = self.path
        return f'Reader({path=}, user={self.user.username})'

    def __iter__(self):
        """Iterates over all the snapshots in the file."""
        snapshot = self.file_reader.get_snapshot()
        while snapshot:
            yield snapshot
            snapshot = self.file_reader.get_snapshot()

    def close(self):
        self.file_reader.stream.close()


def load_readers():
    """
    Loads dynamically all the file readers.

    To add a new reader, add a file to the sub-package 'file_readers'
    with a class named ***Reader, with an attribute named 'prefix' (string),
    which indicates the file format this reader supports.
    """
    root = Path("mindreader/drivers/reader/file_readers").absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, filereader in module.__dict__.items():
            if isinstance(filereader, type) and filereader.__name__.endswith("Reader"):
                supported_file_readers[filereader.prefix] = filereader


load_readers()

import importlib
import sys
from mindreader.objects import User, Snapshot
from pathlib import Path


supported_encoders = {}
"""Holds the list of supported encoders, loaded dynamically."""


class Encoder:
    """
    Allows to encode/decode user and snapshot objects.
    This class serves as an interface to the available encoders.

    To add a new encoder, add a file named <name>_encoder.py to the current-package,
    with a class named <name>Encoder, which has an attribute named 'encoder_type' (string),
    that indicates the encoding method of this class.
    """
    def __init__(self, encoder_type: str):
        """Initializes an encoder."""
        if encoder_type not in supported_encoders:
            raise NotImplementedError(f"Encoder type ('{encoder_type}') is not supported")
        self.encoder = supported_encoders[encoder_type]()

    def user_encode(self, user: User):
        """Serialize user object."""
        return self.encoder.user_encode(user)

    def user_decode(self, encoded_user) -> User:
        """Deserialize user object."""
        return self.encoder.user_decode(encoded_user)

    def snapshot_encode(self, snapshot):
        """Serialize snapshot object."""
        return self.encoder.snapshot_encode(snapshot)

    def snapshot_decode(self, encoded_snapshot) -> Snapshot:
        """Deserialize snapshot object."""
        return self.encoder.snapshot_decode(encoded_snapshot)

    def message_encode(self, user: User, snapshot: Snapshot):
        """Serialize user and snapshot together."""
        return self.encoder.message_encode(user, snapshot)

    def message_decode(self, encoded_user_and_snapshot) -> (User, Snapshot):
        """Deserialize user and snapshot, returns a tuple."""
        return self.encoder.message_decode(encoded_user_and_snapshot)


def load_encoders():
    """Loads dynamically all the available encoders."""
    root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(root.parent))
    for file in root.iterdir():
        if file.name.startswith('_') or file.name == 'encoder.py' or not file.suffix == '.py':
            continue
        module = importlib.import_module(f'{root.name}.{file.stem}', package=root.name)

        for key, encoder in module.__dict__.items():
            if isinstance(encoder, type) and encoder.__name__.endswith("Encoder"):
                supported_encoders[encoder.encoder_type] = encoder


load_encoders()

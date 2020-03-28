import requests

from mindreader.drivers.encoders import PBEncoder
from mindreader.drivers.reader.reader import Reader


encoder = PBEncoder()


def upload_sample(host, port, path):
    """
    Read snapshots from path, and sends it to the server at host:port.
    """
    try:
        reader = Reader(path)  # load sample
    except FileNotFoundError:
        raise FileNotFoundError(f"Upload failed: path does not exist")

    user = reader.get_user()
    snapshot = reader.get_snapshot()
    address = f'http://{host}:{port}/snapshot'
    try:
        requests.post(url=address, data=encoder.message_encode(user, snapshot))
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Upload failed: couldn't post to address")

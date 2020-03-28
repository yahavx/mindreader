import requests

from mindreader.drivers.encoders import PBEncoder
from mindreader.drivers.reader.reader import Reader


encoder = PBEncoder()


def upload_sample(host, port, path):
    """Connects to a server and sends snapshot to it."""
    try:
        reader = Reader(path)  # load sample
    except Exception as e:
        print(f"Couldn't open file: {e}")
        return

    user = reader.get_user()
    snapshot = reader.get_snapshot()
    address = f'http://{host}:{port}/snapshot'
    try:
        requests.post(url=address, data=encoder.message_encode(user, snapshot))
    except requests.exceptions.ConnectionError:
        print(f"Uploading failed: couldn't post to {address}")
    except Exception as e:
        print(f'Uploading failed: {e}')

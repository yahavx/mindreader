import requests

from mindreader.drivers.encoders import PBEncoder
from mindreader.drivers import Reader

encoder = PBEncoder()


def upload_sample(host: str, port: str, path: str):
    """
    Reads snapshots from a file, and sends them to the server.

    Args:
        host(str): host of the server.
        port(str): port of the server.
        path(str): path to the file.

    Raises:
        FileNotFoundError: the path to the file is invalid.
        ConnectionError: couldn't establish connection to the server.
    """
    try:
        reader = Reader(path)  # load sample
    except FileNotFoundError:
        raise FileNotFoundError(f"Client failure: path to sample does not exist")

    user = reader.get_user()
    snapshot = reader.get_snapshot()

    address = generate_snapshot_address(host, port)
    encoded_data = encoder.message_encode(user, snapshot)
    try:
        send_data_to_server(address, encoded_data)
    except ConnectionError:
        raise ConnectionError(f"Client failure: couldn't connect to server")


def send_data_to_server(address, data):
    try:
        requests.post(url=address, data=data)
    except requests.exceptions.ConnectionError:
        raise ConnectionError


def generate_snapshot_address(host: str, port: str) -> str:
    """
    Generates an address from host and port, according to the client-server protocol.
    """
    return f'http://{host}:{port}/snapshot'

import requests

from mindreader.drivers.encoders import PBEncoder
from mindreader.drivers import Reader

encoder = PBEncoder()


def upload_sample(host: str, port: int, path: str, file_format: str = 'pb'):
    """
    Reads snapshots from a file, and sends them to the server.
    If message was received successfully in the server, prints a message.

    Args:
        host(str): host of the server.
        port(int): port of the server.
        path(str): path to the file (relative or absolute).
        file_format(str): the format of the file provided.

    Raises:
        FileNotFoundError: the path to the file is invalid.
        ConnectionError: couldn't establish connection to the server.
    """
    try:
        reader = Reader(path, file_format)  # load sample
    except FileNotFoundError:
        raise FileNotFoundError(f"Client failure: path to sample does not exist")

    user = reader.get_user()
    snapshot = reader.get_snapshot()

    address = generate_snapshot_address(host, port)
    encoded_data = encoder.message_encode(user, snapshot)
    try:
        code = send_data_to_server(address, encoded_data)
        if code == 200:
            print("Message sent successfully")

    except ConnectionError:
        raise ConnectionError(f"Client failure: couldn't connect to server")


def send_data_to_server(address: str, data) -> int:
    """
    Sends a post request to the server.

    Args:
        address(str): full address of the server 'post' page.
        data: data to send.

    Returns:
        Status code of the post request.
    """
    try:
        r = requests.post(url=address, data=data)
        return r.status_code

    except requests.exceptions.ConnectionError:
        raise ConnectionError


def generate_snapshot_address(host: str, port: int) -> str:
    """
    Generates an address from host and port, according to the client-server protocol.
    """
    return f'http://{host}:{port}/snapshot'

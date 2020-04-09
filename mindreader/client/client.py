import requests

from mindreader.drivers.encoders import PBEncoder
from mindreader.drivers import Reader
from mindreader.objects import User, Snapshot

encoder = PBEncoder()


def upload_sample(host: str, port: int, path: str, file_format: str = 'pb'):
    """
    Reads snapshots from a file, and sends them to the server.
    If all the snapshots were sent successfully to the server,
    or the function operation was interrupted, prints an appropriate message.

    :param host: host of the server.
    :param port: port of the server.
    :param path: path to the file (relative or absolute).
    :param file_format: the format of the file provided.

    :raises FileNotFoundError: the path to the file is invalid.
    :raises ConnectionRefusedError: couldn't establish connection to the server.
    :raises ConnectionError: the server sent a bad response code.

    :return: The number of snapshots sent successfully.
    """
    try:
        reader = Reader(path, file_format)  # load sample
    except FileNotFoundError:
        raise FileNotFoundError(f"Client failure: path to sample does not exist")

    user = reader.get_user()
    address = generate_snapshot_address(host, port)

    i = 0

    try:
        for snapshot in reader:
            send_snapshot(address, snapshot, user)
            i += 1
    except ConnectionRefusedError:
        raise ConnectionRefusedError(f"Client failure: couldn't connect to server")
    except ConnectionError:
        raise ConnectionError("Client failure: the server sent back a bad response")
    except KeyboardInterrupt:
        print(f'Some of the snapshots were not sent due to a keyboard interrupt. Total sent: {i}')
    else:
        print(f"All the {i} snapshots were sent successfully!")
    return i


def send_snapshot(address: str, snapshot: Snapshot, user: User):
    """
    Sends a single snapshot to the server.
    """
    encoded_data = encoder.message_encode(user, snapshot)
    try:
        status_code = post_serialized_data_to_server(address, encoded_data)
        if status_code != 200:
            raise ConnectionError

    except ConnectionRefusedError:
        raise ConnectionRefusedError


def post_serialized_data_to_server(address: str, data) -> int:
    """
    Sends a post request to the server.

    :return: Status code of the post request.
    """
    try:
        r = requests.post(url=address, data=data)
        return r.status_code

    except requests.exceptions.ConnectionError:
        raise ConnectionRefusedError


def generate_snapshot_address(host: str, port: int) -> str:
    """
    Generates an address from host and port, according to the client-server protocol.
    """
    return f'http://{host}:{port}/snapshot'

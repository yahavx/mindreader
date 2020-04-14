import uuid

import requests

from mindreader.drivers.encoders import DefaultClientServerProtocolEncoder
from mindreader.drivers import Reader, Encoder
from mindreader.objects import User, Snapshot


def upload_sample(host: str, port: int, path: str, file_format: str = 'protobuf'):
    """
    Reads snapshots from a file, and sends them to the server.
    If all the snapshots were sent successfully to the server,
    or the function operation was interrupted, prints an appropriate message.

    :param host: host of the server.
    :param port: port of the server.
    :param path: path to the file (relative or absolute).
    :param file_format: the format of the file provided, default is 'pb' (protobuf).
    """

    try:
        reader = Reader(path, file_format)  # load sample
    except FileNotFoundError:
        print(f"Client error: path to sample does not exist")
        exit(1)
    except NotImplementedError:
        print("Client error: sample format is not supported")
        exit(1)

    user = reader.get_user()
    i = 0  # count the snapshots sent
    print("Starting to send snapshots...")
    try:
        for snapshot in reader:
            snapshot.metadata.user_id = user.user_id
            snapshot.metadata.snapshot_id = str(uuid.uuid4())  # generate id for the snapshot before sending
            i += 1  # we may count one more sometimes, usually its ok somehow...
            send_snapshot(host, port, snapshot, user)

    except ConnectionRefusedError:
        print("Client error: couldn't connect to server")
        exit(1)
    except ConnectionError:
        print("Client error: the server sent back a bad response")
        exit(1)  # we prefer not to retry to avoid cognition on server
    except KeyboardInterrupt:
        print(f'Some of the snapshots were not sent due to a keyboard interrupt. Total sent: {i}')
    else:
        print(f"All the {i} snapshots were sent successfully!")


def send_snapshot(host: str, port: int, snapshot: Snapshot, user: User):
    """Sends a single snapshot to the server."""
    address = generate_snapshot_address(host, port)
    encoder = Encoder('protobuf')
    encoded_data = encoder.message_encode(user, snapshot)
    try:
        r = requests.post(url=address, data=encoded_data)
    except requests.exceptions.ConnectionError:
        raise ConnectionRefusedError

    if r.status_code != 200:
        raise ConnectionError


def generate_snapshot_address(host: str, port: int) -> str:
    """Generates an address from host and port, according to the client-server protocol."""
    return f'http://{host}:{port}/snapshot'

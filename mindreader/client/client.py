import requests

from mindreader.drivers.encoders import DefaultClientServerProtocolEncoder
from mindreader.drivers import Reader
from mindreader.objects import User, Snapshot


encoder = DefaultClientServerProtocolEncoder()


def upload_sample(host: str, port: int, path: str, file_format: str = 'pb'):
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

    user = reader.get_user()
    address = generate_snapshot_address(host, port)

    i = 0  # count the snapshots sent
    print("Starting to send...")
    try:
        for snapshot in reader:
            send_snapshot(address, snapshot, user)
            i += 1  # we may count one less sometimes...
    except ConnectionRefusedError:
        print("Client error: couldn't connect to server")
        exit(1)
    except ConnectionError:
        print("Client error: the server sent back a bad response")
        exit(1)
    except KeyboardInterrupt:
        print(f'Some of the snapshots were not sent due to a keyboard interrupt. Total sent: {i}')
    else:
        print(f"All the {i} snapshots were sent successfully!")


def send_snapshot(address: str, snapshot: Snapshot, user: User):
    """Sends a single snapshot to the server."""
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

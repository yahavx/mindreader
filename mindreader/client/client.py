import requests
from mindreader.drivers.reader.reader import Reader
from mindreader.drivers.encoders.pb_encoder import PBEncoder

encoder = PBEncoder()


def upload_sample(host, port, path="sample.mind.gz"):
    reader = Reader(path)
    user = reader.get_user()
    snapshot = reader.get_snapshot()
    address = f'http://{host}:{port}/snapshot'
    r = requests.post(url=address, data=encoder.message_encode(user, snapshot))

    if r.status_code != 200:
        print("Snapshot was sent unsuccessfully")

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


def upload_samples(amount):  # TODO: remove
    reader = Reader("sample.mind.gz")
    user = reader.get_user()
    i = 0
    for snapshot in reader:
        r = requests.post(url="http://127.0.0.1:8000/snapshot", data=encoder.message_encode(user, snapshot))
        i += 1
        if i == amount:
            break

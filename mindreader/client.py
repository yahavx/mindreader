import requests
from mindreader.drivers.reader.reader import Reader
from mindreader.drivers.protocol_encoder.pb_encoder import PBEncoder


def snap():
    r = Reader("sample.mind.gz")
    return r.get_snapshot()


def read2():
    return Reader("sample.mind.gz")


def upload_sample(host, port, path="sample.mind.gz"):
    reader = Reader(path)
    user = reader.get_user()
    snapshot = reader.get_snapshot()
    address = f'http://{host}:{port}/snapshot'
    # config = get_config(address)
    r = requests.post(url=address, data=PBEncoder.message_encode(user, snapshot))


# def get_config(address):
#     r = requests.get(url=HTTP + address + "/config")
#     return r.json()

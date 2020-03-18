import requests
from mindreader.utils.reader.reader import Reader
from mindreader.utils.protocol_encoder.pb_encoder import PBEncoder


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


# def parse_color_image(snapshot):
#     path = './color_image.jpg'
#     size = snapshot.color_image.width, snapshot.color_image.height
#     # print('\n\n\n\n')
#     # print(size)
#     # print(len(snapshot.color_image.data))
#     # print('\n\n\n\n')
#     from PIL import Image as PIL
#     image = PIL.new('RGB', size)
#     data = snapshot.color_image.data
#     print(data[0:10])
#     print(len(data))
#     image.putdata(snapshot.color_image.data[1:])
#     image.save(path)

import requests
import json
from mindreader.objects import User
from mindreader.utils.reader.reader import Reader
from mindreader.objects.snapshot import Snapshot, Pose, Translation, Rotation, Image, Feelings

HTTP = "http://"
MINDREADER_FILE = "/home/user/YahavFooBar/sample.mind.gz"


def snap_encode(snapshot):
    # result = json.dumps(snapshot, cls=ComplexEncoder)
    result = json.dumps(snapshot, default=lambda o: o.__dict__ if type(o) != bytes else o.hex(), indent=4)
    return result


def snap_decode(json_snapshot):
    snap = json.loads(json_snapshot)
    # snap = json_snapshot
    timestamp = snap["timestamp"]
    pose = Pose(Translation(**snap["pose"]["translation"]), Rotation(**snap["pose"]["rotation"]))
    color_image = Image(**snap["color_image"])
    color_image.data = bytes.fromhex(color_image.data)
    depth_image = Image(**snap["depth_image"])
    feelings = Feelings(**snap["feelings"])

    return Snapshot(timestamp, pose, color_image, depth_image, feelings)


def user_encode(user):
    return snap_encode(user)


def user_decode(user):
    return User(**json.loads(user))


def upload_sample(host, port, path):
    reader = Reader(path)
    user = reader.get_user_information()
    snapshot = reader.get_snapshot()
    # parse_color_image(snapshot)
    # return
    address = f'{host}:{port}'
    config = get_config(address)
    r = requests.post(url=HTTP + address + "/snapshot", data=json.dumps([snap_encode(user), snap_encode(snapshot)]))


def get_config(address):
    r = requests.get(url=HTTP + address + "/config")
    return r.json()


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
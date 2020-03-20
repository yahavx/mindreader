import json
from bci.objects import User
from bci.objects import Snapshot, Pose, Translation, Rotation, Image, Feelings


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

import gzip
import struct

from mindreader.objects.user import User
from mindreader.objects.snapshot import Snapshot, Pose, Translation, Rotation, Image, Feelings
from mindreader.utils.cortex_pb2 import User as ProtoUser
from mindreader.utils.cortex_pb2 import Snapshot as ProtoSnapshot

UINT_SIZE = 4


class ProtobufFileReader:
    def __init__(self, path=None):
        self.path = path
        if path:
            self.stream = gzip.open(path, "rb")

    def open_file(self, path):
        self.path = path
        self.stream = gzip.open(path, "rb")

    def _get_data(self):
        size, = struct.unpack('I', self.stream.read(UINT_SIZE))
        return self.stream.read(size)

    def get_user_information(self):
        user_snap = ProtoUser()
        user_snap.ParseFromString(self._get_data())
        gender = 'm' if user_snap.gender == 0 else ('f' if user_snap.gender == 1 else 'unknown')
        return user_snap
        return User(user_snap.user_id, user_snap.username, user_snap.birthday, gender)

    @staticmethod
    def _convert_to_snapshot(proto_snap):  # converts proto snapshot to our snapshot object
        tran = proto_snap.pose.translation
        rot = proto_snap.pose.rotation
        pose = Pose(Translation(tran.x, tran.y, tran.z), Rotation(rot.x, rot.y, rot.z, rot.w))

        c_image = proto_snap.color_image
        color_image = Image(c_image.width, c_image.height, c_image.data)
        d_image = proto_snap.depth_image
        depth_image = Image(d_image.width, d_image.height, list(d_image.data))
        feel = proto_snap.feelings
        feelings = Feelings(feel.hunger, feel.thirst, feel.exhaustion, feel.happiness)
        return Snapshot(proto_snap.datetime, pose, color_image, depth_image, feelings)

    def get_snapshot(self):
        proto_snap = ProtoSnapshot()
        proto_snap.ParseFromString(self._get_data())
        return proto_snap
        return self._convert_to_snapshot(proto_snap)

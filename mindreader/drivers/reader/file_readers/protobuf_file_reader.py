import gzip
import struct

from .cortex_pb2 import User as ProtobufUser
from .cortex_pb2 import Snapshot as ProtobufSnapshot
from mindreader.objects import User, Snapshot
from mindreader.objects.snapshot_utils import Pose, Rotation, Translation, Feelings, Image, SnapshotMetadata

UINT_SIZE = 4


class ProtobufFileReader:
    prefix = 'protobuf'

    def __init__(self, path=None):
        self.path = path
        if path:
            self.stream = gzip.open(path, "rb")

    def open_file(self, path):
        """Loads a file from the path."""
        self.path = path
        self.stream = gzip.open(path, "rb")

    def _get_data(self) -> bytes:
        """Reads 4 bytes, parses it to an integer, and returns the following <number> bytes."""
        size, = struct.unpack('I', self.stream.read(UINT_SIZE))
        return self.stream.read(size)

    def get_user(self) -> User:
        """Returns the user of the snapshots in the stream."""
        pb_user = ProtobufUser()
        pb_user.ParseFromString(self._get_data())
        gender = 'male' if pb_user.gender == 0 else 'female' if pb_user.gender == '1' else 'unknown'
        return User(pb_user.user_id, pb_user.username, pb_user.birthday, gender)

    def get_snapshot(self) -> Snapshot:
        """Returns the next snapshot in the stream."""
        pb_snapshot = ProtobufSnapshot()
        pb_snapshot.ParseFromString(self._get_data())

        snapshot = _convert_pb_to_snapshot(pb_snapshot)

        return snapshot


def _convert_pb_to_snapshot(snap: ProtobufSnapshot) -> Snapshot:
    """Converts protobuf snapshot to project snapshot object."""
    translation = Translation(snap.pose.translation.x, snap.pose.translation.y, snap.pose.translation.z)
    rotation = Rotation(snap.pose.rotation.x, snap.pose.rotation.y, snap.pose.rotation.z, snap.pose.rotation.w)
    pose = Pose(translation, rotation)
    color_image = Image(snap.color_image.width, snap.color_image.height, snap.color_image.data)
    depth_image = Image(snap.depth_image.width, snap.depth_image.height, snap.depth_image.data)
    feelings = Feelings(snap.feelings.hunger, snap.feelings.thirst, snap.feelings.exhaustion, snap.feelings.happiness)
    metadata = SnapshotMetadata(timestamp=snap.datetime)
    snapshot = Snapshot(pose, color_image, depth_image, feelings, metadata)

    return snapshot

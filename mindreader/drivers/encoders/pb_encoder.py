import struct
import io

from .mindreader_pb2 import ProtoUser  # not to be mistaken with cortex protobuf
from .mindreader_pb2 import ProtoSnapshot
from mindreader.objects import User, Snapshot
from mindreader.objects.snapshot_utils import Pose, Translation, Rotation, Image, Feelings, SnapshotMetadata


class PBEncoder:
    """Encodes user and snapshot objects using protobuf."""

    encoder_type = 'protobuf'

    def user_encode(self, user: User) -> bytes:
        pb_user = ProtoUser()
        pb_user.user_id = user.user_id
        pb_user.username = user.username
        pb_user.birthday = user.birthday
        pb_user.gender = user.gender
        return pb_user.SerializeToString()

    def user_decode(self, user_bytes: bytes) -> User:
        pb_user = ProtoUser()
        pb_user.ParseFromString(user_bytes)
        user = User(pb_user.user_id, pb_user.username, pb_user.birthday, pb_user.gender)
        return user

    def snapshot_encode(self, snapshot: Snapshot) -> bytes:
        pb_snapshot = ProtoSnapshot()

        pb_snapshot.pose.translation.x = snapshot.pose.translation.x
        pb_snapshot.pose.translation.y = snapshot.pose.translation.y
        pb_snapshot.pose.translation.z = snapshot.pose.translation.z

        pb_snapshot.pose.rotation.x = snapshot.pose.rotation.w
        pb_snapshot.pose.rotation.y = snapshot.pose.rotation.y
        pb_snapshot.pose.rotation.z = snapshot.pose.rotation.z
        pb_snapshot.pose.rotation.w = snapshot.pose.rotation.w

        pb_snapshot.color_image.width = snapshot.color_image.width
        pb_snapshot.color_image.height = snapshot.color_image.height
        pb_snapshot.color_image.data = snapshot.color_image.data

        pb_snapshot.depth_image.width = snapshot.depth_image.width
        pb_snapshot.depth_image.height = snapshot.depth_image.height
        pb_snapshot.depth_image.data.extend(snapshot.depth_image.data)

        pb_snapshot.feelings.hunger = snapshot.feelings.hunger
        pb_snapshot.feelings.thirst = snapshot.feelings.thirst
        pb_snapshot.feelings.exhaustion = snapshot.feelings.exhaustion
        pb_snapshot.feelings.happiness = snapshot.feelings.happiness

        pb_snapshot.metadata.timestamp = snapshot.metadata.timestamp
        pb_snapshot.metadata.user_id = snapshot.metadata.user_id
        pb_snapshot.metadata.snapshot_id = snapshot.metadata.snapshot_id

        return pb_snapshot.SerializeToString()

    def snapshot_decode(self, snapshot_bytes: bytes) -> Snapshot:
        pb_snapshot = ProtoSnapshot()
        pb_snapshot.ParseFromString(snapshot_bytes)
        translation = Translation(pb_snapshot.pose.translation.x, pb_snapshot.pose.translation.y,
                                  pb_snapshot.pose.translation.z)
        rotation = Rotation(pb_snapshot.pose.rotation.x, pb_snapshot.pose.rotation.y, pb_snapshot.pose.rotation.z,
                            pb_snapshot.pose.rotation.w)
        pose = Pose(translation, rotation)
        color_image = Image(pb_snapshot.color_image.width, pb_snapshot.color_image.height, pb_snapshot.color_image.data)
        depth_image = Image(pb_snapshot.depth_image.width, pb_snapshot.depth_image.height, pb_snapshot.depth_image.data)
        feelings = Feelings(pb_snapshot.feelings.hunger, pb_snapshot.feelings.thirst, pb_snapshot.feelings.exhaustion,
                            pb_snapshot.feelings.happiness)
        metadata = SnapshotMetadata(pb_snapshot.metadata.timestamp, pb_snapshot.metadata.user_id,
                                    pb_snapshot.metadata.snapshot_id)
        snapshot = Snapshot(pose, color_image, depth_image, feelings, metadata)

        return snapshot

    def message_encode(self, user: User, snapshot: Snapshot):
        user_bytes = self.user_encode(user)
        snapshot_bytes = self.snapshot_encode(snapshot)
        user_len = struct.pack('I', len(user_bytes))
        snapshot_len = struct.pack('I', len(snapshot_bytes))
        return user_len + user_bytes + snapshot_len + snapshot_bytes

    def message_decode(self, message_bytes) -> (User, Snapshot):
        stream = io.BytesIO(message_bytes)
        user_len, = struct.unpack('I', stream.read(4))
        user_bytes = stream.read(user_len)
        snapshot_len, = struct.unpack('I', stream.read(4))
        snapshot_bytes = stream.read(snapshot_len)

        user = self.user_decode(user_bytes)
        snapshot = self.snapshot_decode(snapshot_bytes)

        return user, snapshot

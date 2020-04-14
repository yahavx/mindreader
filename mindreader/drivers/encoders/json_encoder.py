import json

from mindreader.objects import User, Snapshot
from mindreader.objects.snapshot_utils import Pose, Image, Feelings, Rotation, Translation, SnapshotMetadata


class JSONEncoder:
    """
    Encodes user and snapshot objects using JSON.
    For snapshot encoding, the snapshot must not contain binary data,
    or any non JSON-friendly type (except the snapshot self classes).
    """

    encoder_type = 'json'

    def user_encode(self, user: User) -> str:
        json_user = json.dumps(user.__dict__, indent=4)
        return json_user

    def user_decode(self, json_user: str) -> User:
        json_loaded_user = json.loads(json_user)
        user = User(**json_loaded_user)
        return user

    def snapshot_encode(self, snapshot: Snapshot) -> str:
        json_snapshot = json.dumps(snapshot, default=lambda cls: cls.__dict__, indent=4)
        return json_snapshot

    def snapshot_decode(self, json_snapshot) -> Snapshot:
        json_loaded_snapshot = json.loads(json_snapshot)

        translation = Translation(**json_loaded_snapshot["pose"]["translation"])
        rotation = Rotation(**json_loaded_snapshot["pose"]["rotation"])
        pose = Pose(translation, rotation)
        color_image = Image(**json_loaded_snapshot["color_image"])
        depth_image = Image(**json_loaded_snapshot["depth_image"])
        feelings = Feelings(**json_loaded_snapshot["feelings"])
        metadata = SnapshotMetadata(**json_loaded_snapshot["metadata"])

        snapshot = Snapshot(pose, color_image, depth_image, feelings, metadata)
        return snapshot

    def message_encode(self, user: User, snapshot: Snapshot):
        json_user = self.user_encode(user)
        json_snapshot = self.snapshot_encode(snapshot)
        message = json.dumps({'user': json_user, 'snapshot': json_snapshot})
        return message

    def message_decode(self, json_message) -> (User, Snapshot):
        message = json.loads(json_message)
        user = self.user_decode(message['user'])
        snapshot = self.snapshot_decode(message['snapshot'])
        return user, snapshot

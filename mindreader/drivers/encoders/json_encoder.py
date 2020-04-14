import json

from mindreader.objects import User, Snapshot
from mindreader.objects.snapshot_utils import Pose, Image, Feelings, SnapshotMetadata


class JSONEncoder:
    """
    Encodes user and snapshot objects using JSON.
    For snapshot encoding, the snapshot must not contain binary data,
    or any non JSON-friendly type (except the snapshot self classes).
    """

    encoder_type = 'json'

    def user_encode(self, user):
        return json.dumps(user.__dict__, indent=4)

    def user_decode(self, json_user):
        return json.loads(json_user)

    def snapshot_encode(self, snapshot):
        return json.dumps(snapshot.__dict__, indent=4)

    def snapshot_decode(self, json_snapshot):
        return json.loads(json_snapshot)

    def message_encode(self, user: User, snapshot: Snapshot):
        raise NotImplementedError("Message encode is not implemented in JSON")

    def message_decode(self, message_bytes) -> (User, Snapshot):
        raise NotImplementedError("Message decode is not implemented in JSON")

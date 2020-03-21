import struct
import io
from mindreader.objects.cortex_pb2 import User
from mindreader.objects.cortex_pb2 import Snapshot


class PBEncoder:
    def user_encode(self, user):
        return user.SerializeToString()

    def user_decode(self, user_bytes):
        user = User()
        user.ParseFromString(user_bytes)
        return user

    def snapshot_encode(self, snapshot):
        return snapshot.SerializeToString()

    def snapshot_decode(self, snapshot_bytes):
        snapshot = Snapshot()
        snapshot.ParseFromString(snapshot_bytes)
        return snapshot

    def message_encode(self, user, snapshot):
        user_bytes = self.user_encode(user)
        snapshot_bytes = self.snapshot_encode(snapshot)
        user_len = struct.pack('I', len(user_bytes))
        snapshot_len = struct.pack('I', len(snapshot_bytes))
        return user_len + user_bytes + snapshot_len + snapshot_bytes

    def message_decode(self, message_bytes):
        stream = io.BytesIO(message_bytes)
        user_len, = struct.unpack('I', stream.read(4))
        user_bytes = stream.read(user_len)
        snapshot_len, = struct.unpack('I', stream.read(4))
        snapshot_bytes = stream.read(snapshot_len)

        user = self.user_decode(user_bytes)
        snapshot = self.snapshot_decode(snapshot_bytes)

        return [user, snapshot]

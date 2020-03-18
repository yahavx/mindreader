import struct
import io
from mindreader.utils.cortex_pb2 import User as ProtoUser
from mindreader.utils.cortex_pb2 import Snapshot as ProtoSnapshot


class PBMQEncoder:  # this class can decode user and snapshot to bytes
    @staticmethod
    def user_encode(user):
        return user.SerializeToString()
    
    @staticmethod
    def user_decode(user_bytes):
        user = ProtoUser()
        user.ParseFromString(user_bytes)
        return user

    @staticmethod
    def snapshot_encode(snapshot):
        return snapshot.SerializeToString()

    @staticmethod
    def snapshot_decode(snapshot_bytes):
        snapshot = ProtoSnapshot()
        snapshot.ParseFromString(snapshot_bytes)
        return snapshot

    @staticmethod
    def message_encode(user, snapshot):
        user_bytes = PBMQEncoder.user_encode(user)
        snapshot_bytes = PBMQEncoder.snapshot_encode(snapshot)
        user_len = struct.pack('I', len(user_bytes))
        snapshot_len = struct.pack('I', len(snapshot_bytes))
        return user_len + user_bytes + snapshot_len + snapshot_bytes

    @staticmethod
    def message_decode(message_bytes):
        stream = io.BytesIO(message_bytes)
        user_len, = struct.unpack('I', stream.read(4))
        user_bytes = stream.read(user_len)
        snapshot_len, = struct.unpack('I', stream.read(4))
        snapshot_bytes = stream.read(snapshot_len)

        user = PBMQEncoder.user_decode(user_bytes)
        snapshot = PBMQEncoder.snapshot_decode(snapshot_bytes)

        return [user, snapshot]

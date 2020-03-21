import gzip
import struct
from mindreader.objects.cortex_pb2 import User
from mindreader.objects.cortex_pb2 import Snapshot

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
        user_snap = User()
        user_snap.ParseFromString(self._get_data())
        return user_snap

    def get_snapshot(self):
        proto_snap = Snapshot()
        proto_snap.ParseFromString(self._get_data())
        return proto_snap

import struct
import datetime as dt

UINT_SIZE = 4
ULONG_SIZE = 8
FLOAT = 4
DOUBLE = 8

class Snapshot:
    pass


class Reader:
    def __init__(self, path):
        self.path = path
        self.stream = open(path, "rb")
        self.user_id = None

    def __repr__(self):
        if self.user_id is None:  # not initialized
            return "Reader()"
        user_id = self.user_id
        username = self.username
        birthdate = dt.datetime.fromtimestamp(self.birthdate)
        return f'Reader({user_id=}, {username=}, {birthdate=})'
        name_r = f'Name = '

    def get_user_information(self):
        s = self.stream
        self.user_id, = struct.unpack('Q', s.read(ULONG_SIZE))
        username_len, = struct.unpack('I', s.read(UINT_SIZE))
        self.username = s.read(username_len).decode('utf8')
        self.birthdate, = struct.unpack('I', s.read(UINT_SIZE))

    def get_snapshot(self):
        s = self.stream
        snapshot = Snapshot()
        snapshot.timestamp, = struct.unpack('Q', s.read(ULONG_SIZE))
        snapshot.translation = struct.unpack('ddd', s.read(DOUBLE*3))
        snapshot.rotation = struct.unpack('dddd', s.read(DOUBLE * 4))

        c_image_height, = struct.unpack('I', s.read(UINT_SIZE))
        c_image_width, = struct.unpack('I', s.read(UINT_SIZE))
        color_image = list()
        for i in range(c_image_height):
            color_image.append(s.read(3 * c_image_width))
        snapshot.color_image = color_image

        d_image_height, = struct.unpack('I', s.read(UINT_SIZE))
        d_image_width, = struct.unpack('I', s.read(UINT_SIZE))
        depth_image = list()
        for i in range(d_image_height):
            depth_image.append(struct.unpack('f'*d_image_width, s.read(FLOAT)))
        snapshot.depth_image = depth_image

        snapshot.hunger, = struct.unpack('f', s.read(FLOAT))
        snapshot.thirst, = struct.unpack('f', s.read(FLOAT))
        snapshot.exhaustion, = struct.unpack('f', s.read(FLOAT))
        snapshot.happiness, = struct.unpack('f', s.read(FLOAT))


sample = "./sample.mind"
reader = Reader(sample)
print(f'{reader!r}')
reader.get_user_information()
print(f'{reader!r}')
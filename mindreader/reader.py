import struct
import datetime as dt

from mindreader.snapshot import Snapshot


UINT_SIZE = 4
ULONG_SIZE = 8
FLOAT = 4
DOUBLE = 8


class Reader:
    def __init__(self, path):
        self.path = path
        self.stream = open(path, "rb")
        self._get_user_information()

    def __repr__(self):
        user_id = self.user_id
        username = self.username
        birthdate = dt.datetime.fromtimestamp(self.birthdate).strftime("%d/%m/%y")
        gender = self.gender
        return f'Reader({user_id=}, {username=}, {birthdate=}, {gender=})'

    def __str__(self):
        user = f'user {self.user_id}'
        birthdate = dt.datetime.fromtimestamp(self.birthdate).strftime("%d/%m/%y")
        gender = 'male' if gender == 'm' else "female"
        return f'{user}: {self.username}, born {birthdate} ({gender})'

    def _get_user_information(self):
        s = self.stream
        self.user_id, = struct.unpack('Q', s.read(ULONG_SIZE))
        username_len, = struct.unpack('I', s.read(UINT_SIZE))
        self.username = s.read(username_len).decode('utf8')
        self.birthdate, = struct.unpack('I', s.read(UINT_SIZE))
        self.gender, = s.read(1).decode('utf8')

    def get_snapshot(self):
        s = self.stream
        snapshot = Snapshot()

        first_token = s.read(ULONG_SIZE)
        if not first_token:  # reached EOF
            return None

        snapshot.timestamp, = struct.unpack('Q', first_token)
        snapshot.translation = struct.unpack('ddd', s.read(3 * DOUBLE))
        snapshot.rotation = struct.unpack('dddd', s.read(4 * DOUBLE))

        ci_height, = struct.unpack('I', s.read(UINT_SIZE))
        ci_width, = struct.unpack('I', s.read(UINT_SIZE))
        color_image = list()
        for i in range(ci_height):
            color_image.append(s.read(3 * ci_width))
        snapshot.ci_height = ci_height
        snapshot.ci_width = ci_width
        snapshot.color_image = color_image

        di_height, = struct.unpack('I', s.read(UINT_SIZE))
        di_width, = struct.unpack('I', s.read(UINT_SIZE))
        depth_image = list()
        for i in range(di_height):
            depth_image.append(struct.unpack('f'*di_width, s.read(di_width * FLOAT)))
        snapshot.di_height = ci_height
        snapshot.di_width = ci_width
        snapshot.depth_image = depth_image

        snapshot.hunger, = struct.unpack('f', s.read(FLOAT))
        snapshot.thirst, = struct.unpack('f', s.read(FLOAT))
        snapshot.exhaustion, = struct.unpack('f', s.read(FLOAT))
        snapshot.happiness, = struct.unpack('f', s.read(FLOAT))
        return snapshot

    def __iter__(self):
        while True:
            snapshot = self.get_snapshot()
            if not snapshot:  # reached EOF
                break
            yield snapshot

    def close(self):
        self.stream.close()

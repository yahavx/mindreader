import struct
from datetime import datetime


class Thought:
    """Represents a thought of a user"""
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        user_id_r = f'user_id={self.user_id!r}'
        timestamp_r = f'timestamp={self.timestamp!r}'
        thought_r = f'thought={self.thought!r}'
        return f'Thought({user_id_r}, {timestamp_r}, {thought_r})'

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        if self.user_id != other.user_id:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.thought != other.thought:
            return False
        return True

    def serialize(self):
        """Converts a thought to byte format"""
        user_bytes = struct.pack('Q', self.user_id)
        timestamp_bytes = struct.pack('Q', int(datetime.timestamp(self.timestamp)))
        msg_len_bytes = struct.pack('I', len(self.thought))
        msg_bytes = self.thought.encode('utf8')
        return user_bytes + timestamp_bytes + msg_len_bytes + msg_bytes

    @staticmethod
    def deserialize(data):
        """Converts a sequence of bytes to a thought"""
        user_id = struct.unpack('Q', data[0:8])[0]
        timestamp = struct.unpack('Q', data[8:16])[0]
        n = struct.unpack('I', data[16:20])[0]
        thought = data[20:20+n].decode('utf8')
        timestamp = datetime.fromtimestamp(timestamp)
        return Thought(user_id, timestamp, thought)

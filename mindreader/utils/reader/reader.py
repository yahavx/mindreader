from .protobuf_file_reader import ProtobufFileReader

DEFAULT_PARSER = ProtobufFileReader


class Reader:
    def __init__(self, path, file_reader=None):
        self.path = path
        if not file_reader:
            file_reader = DEFAULT_PARSER()
        self.file_reader = file_reader

        self.file_reader.open_file(path)
        self.user = self.file_reader.get_user_information()

    def get_user_information(self):
        return self.user

    def get_snapshot(self):
        return self.file_reader.get_snapshot()

    def __repr__(self):
        path = self.path
        return f'Reader({path=}, user={self.user.username})'

    def __str__(self):
        path = self.path
        return f'Reader({path=}, user={self.user.username})'

    def __iter__(self):
        while True:
            snapshot = self.file_reader.get_snapshot()
            if not snapshot:  # reached EOF
                break
            yield snapshot

    def close(self):
        self.file_reader.stream.close()

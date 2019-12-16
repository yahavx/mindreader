import socket
import struct
from mindreader.reader import UINT_SIZE


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        sock = self.socket.getsockname()
        peer = self.socket.getpeername()
        return f'<Connection from {sock[0]}:{sock[1]} to {peer[0]}:{peer[1]}>'

    def send_message(self, data):
        self.socket.sendall(data)

    def receive_message(self):
        x = b''
        size, = struct.unpack('I', self.socket.read(UINT_SIZE))
        original_size = size
        while size > 0:
            tmp = self.socket.recv(size)
            if not tmp:
                raise Exception(f'Could not read {original_size} bytes')
            size -= len(tmp)
            x += tmp
        return x

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def connect(cls, ip, port):
        sock = socket.socket()
        sock.connect((ip, port))
        return Connection(sock)

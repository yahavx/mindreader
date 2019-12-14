from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.server = socket.socket()

    def __repr__(self):
        port_r = f'port={self.port!r}'
        host_r = f'host={self.host!r}'
        backlog_r = f'backlog={self.backlog!r}'
        reuseaddr_r = f'reuseaddr={self.reuseaddr!r}'
        return f'Listener({port_r}, {host_r}, {backlog_r}, {reuseaddr_r})'

    def start(self):
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)

    def stop(self):
        self.server.close()

    def accept(self):
        client_socket, address = self.server.accept()
        return Connection(client_socket)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

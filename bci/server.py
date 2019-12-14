import os
import struct
import threading
from .utils.listener import Listener
from .utils.connection import Connection
from .thought import Thought
from .cli import CommandLineInterface

cli = CommandLineInterface()

data_directory = ''


class ServerThread(threading.Thread):
    lock = threading.Lock()

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        data = self.client.receive(20)
        n = struct.unpack('I', data[16:20])[0]
        data += self.client.receive(n)

        full_thought = Thought.deserialize(data)

        time = str(full_thought.timestamp)
        time = time.replace(' ', '_')
        time = time.replace(':', '-')

        folder = f'{data_directory}/{full_thought.user_id}'
        file = f'{folder}/{time}.txt'

        self.lock.acquire()
        try:
            if not os.path.isdir(folder):
                os.makedirs(folder)  # folder doesn't exist, create it

            if not os.path.isfile(file):  # file doesn't exist
                file = open(file, 'w')
            else:
                file = open(file, 'a')
                file.write('\n')
            file.write(full_thought.thought)
            file.close()
        finally:
            self.lock.release()

    def get_bytes(self, n):
        x = b''
        client = self.client
        while n > 0:
            tmp = client.recv(n)
            if not tmp:
                raise Exception(f'Could not read {n} bytes')
            n -= len(tmp)
            x += tmp
        return x


@cli.command
def run_server(address, data):
    global data_directory
    data_directory = data
    ip, port = address.split(':')
    listener = Listener(int(port), host=ip)
    listener.start()

    while True:
        try:
            client = listener.accept()
            handler = ServerThread(client)
            handler.start()

        except KeyboardInterrupt:
            print('Server terminated by user (KeyboardInterrupt)')
            return 0


if __name__ == '__main__':
    import sys
    sys.exit(cli.main())

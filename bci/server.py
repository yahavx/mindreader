import os
import struct
import threading
from .utils.listener import Listener
from .thought import Thought


def run_server(address, data_dir):
    listener = Listener(address[1], host=address[0])
    with listener:
        while True:
            client = listener.accept()
            handler = ServerThread(client, data_dir)
            handler.start()


class ServerThread(threading.Thread):
    lock = threading.Lock()

    def __init__(self, client, data_dir):
        super().__init__()
        self.client = client
        self.data_dir = data_dir

    def run(self):
        data = self.client.receive(20)
        n = struct.unpack('I', data[16:20])[0]
        data += self.client.receive(n)

        full_thought = Thought.deserialize(data)

        time = str(full_thought.timestamp)
        time = time.replace(' ', '_')
        time = time.replace(':', '-')

        folder = f'{self.data_dir}/{full_thought.user_id}'
        file = f'{folder}/{time}.txt'

        with self.lock:
            if not os.path.isdir(folder):
                os.makedirs(folder)  # folder doesn't exist, create it

            if not os.path.isfile(file):  # file doesn't exist
                file = open(file, 'w')
            else:
                file = open(file, 'a')
                file.write('\n')
            file.write(full_thought.thought)
            file.close()

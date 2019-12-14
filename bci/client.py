import socket
import struct
from .cli import CommandLineInterface
from .thought import Thought
from .utils.connection import Connection
import datetime
import time

cli = CommandLineInterface()


@cli.command
def upload_thought(address, user, thought):
    ip, port = address.split(':')
    port = int(port)
    try:
        conn = socket.socket()
        conn.connect((ip, port))
        conn = Connection(conn)

        user = int(user)
        timestamp = datetime.datetime.fromtimestamp(int(time.time()))
        full_thought = Thought(user, timestamp, thought)

        conn.send(full_thought.serialize())
        print('done')
        conn.close()

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(cli.main())

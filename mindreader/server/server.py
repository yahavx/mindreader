import sys
from flask import Flask, request

from mindreader.drivers.context import Context
from mindreader.drivers import Encoder
from mindreader.drivers import MessageQueue
from mindreader.objects.snapshot import Snapshot


serv = Flask(__name__)
message_handler = None
mq: MessageQueue = None
data_directory: str = ''


def run_server(host, port, publish=None, mq_url=None, data_dir=None):
    """
    Runs the server, waiting to receive snapshots and handles them,
    either by a self-made handler, or by posting them to the message queue.

    To run with a self-handler, publish should be supplied (see parameter for details below).
    To register to queue, mq_url should be supplied.
    Only and exactly one should be supplied in a call, otherwise its an error.

    :param host: server host.
    :param port: server port.
    :param publish: handler for snapshots, a function that receive a (user, snapshot) and process them.
    :param mq_url: a url to a message queue, to post snapshots on.
    :param data_dir: if the message queue is used, some snapshot data may be saved to this directory.
                     if not supplied, the default is the project root directory under 'mindreader_internal_data'.

    :raises EnvironmentError: publish or mq_url were supplied in correctly.
    :raises ConnectionError: couldn't connect to queue.
    """

    if (publish is not None and mq_url is not None) or (publish is None and mq_url is None):
        raise EnvironmentError("Server error: handler or mq_url should be supplied, and only one of them")

    if publish is not None:
        global message_handler
        message_handler = publish

    else:  # mq is not None
        global mq, data_directory
        try:
            mq = MessageQueue(mq_url)
        except ConnectionError:
            raise ConnectionError("Server error: couldn't connect to message queue")
        if data_dir:
            data_directory = data_dir

    serv.run(host, int(port))


@serv.route('/snapshot', methods=['POST'])
def post_snapshot():
    """
    Handles the post requests of the snapshots.

    :raises PermissionError: tried to save snapshot data to a path without a permission.
    :raises ConnectionError: connection to the message queue to lost.
    """

    message_bytes = request.get_data()

    encoder = Encoder('protobuf')
    user, snapshot = encoder.message_decode(message_bytes)

    if message_handler:  # run_server was invoked through API
        message_handler(user, snapshot)
        return ""

    try:
        context = Context.generate_context_from_snapshot_metadata(snapshot.metadata, data_directory)
    except PermissionError:
        raise PermissionError("Server error: no permission to save data, check context saving location")

    replace_large_data_with_metadata(snapshot, context)

    encoder = Encoder('json')
    user = encoder.user_encode(user)
    snapshot = encoder.snapshot_encode(snapshot)

    try:
        mq.publish('user', user)
        mq.publish('snapshot', snapshot)
    except ConnectionError:
        raise ConnectionError("Server error: connection to message queue was lost")

    return "", 200


def replace_large_data_with_metadata(snapshot: Snapshot, context: Context):
    """
    Saves the large parts of the snapshot to storage (i.e. images),
    and replaces them with metadata (path).

    :param snapshot: snapshot to process
    :param context: initialized context object, to save the data
    """
    color_image_data = snapshot.color_image.data
    depth_image_data = list(snapshot.depth_image.data)
    snapshot.color_image.data = context.save('color_image', color_image_data)
    snapshot.depth_image.data = context.save('depth_image', depth_image_data, is_json=True)

import json
import uuid

from ..drivers.context import Context
from ..drivers.encoders.pb_encoder import PBEncoder
from ..drivers.encoders.json_encoder import JSONEncoder
from ..drivers.message_queues import init_queue
from ..objects.snapshot import Snapshot
from ..objects.user import User
from flask import Flask, request


serv = Flask(__name__)
data_dir = '/home/user/mindreader/data'  # large files will be stored here (path will be passed)
message_handler = None
url = None
protocol_encoder = PBEncoder()
json_encoder = JSONEncoder()


def run_server(host, port, publish=None, mq_url=None):
    if publish:
        global message_handler
        message_handler = publish
    else:
        global url
        url = mq_url
    serv.run(host, int(port))


@serv.route('/snapshot', methods=['POST'])
def post_snapshot():
    message_bytes = request.get_data()
    user, snapshot = protocol_encoder.message_decode(message_bytes)  # convert from bytes to pb objects

    color_image_data = snapshot.color_image.data
    depth_image_data = json.dumps(list(snapshot.depth_image.data))

    user, snapshot = _convert_objects_format(user, snapshot)  # convert objects format to a JSON-supported one
    context = Context(data_dir, user.user_id, snapshot.snapshot_id)
    snapshot.color_image_path = context.save('color_image', color_image_data)
    snapshot.depth_image_path = context.save('depth_image', depth_image_data)

    if message_handler:  # run_server was invoked through API
        message_handler(message_bytes)
        return ""  # return status code 200

    user = json_encoder.user_encode(user)
    snapshot = json_encoder.snapshot_encode(snapshot)

    mq = init_queue(url)
    mq.publish('snapshot', snapshot)

    print("Finished!")
    return ""


def _convert_objects_format(user, snapshot):  # converts user and snapshot from protobuf format to self-created format
    snapshot_id = str(uuid.uuid4())
    snapshot = Snapshot(user.user_id, snapshot_id, snapshot.datetime, snapshot.pose, '', snapshot.color_image.width,
                        snapshot.color_image.height, '', snapshot.depth_image.width, snapshot.depth_image.height,
                        snapshot.feelings)
    gender = 'm' if user.gender == 0 else 'f' if user.gender == '1' else 'u'
    user = User(user.user_id, user.username, user.birthday, gender)
    return user, snapshot

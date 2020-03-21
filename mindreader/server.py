from mindreader.drivers.encoders.pb_encoder import PBEncoder
from mindreader.drivers.message_queues import init_queue
from mindreader.objects.snapshot import Snapshot
from mindreader.objects.user import User
from flask import Flask, request
import uuid


serv = Flask(__name__)
data_dir = '/mindreader_data/'
message_handler = None
url = None
encoder = PBEncoder()


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

    if message_handler:  # run_server was invoked through API
        message_handler(message_bytes)
        return ""  # return status code 200

    user, snapshot = encoder.message_decode(message_bytes)
    user, snapshot = _convert_objects_format(user, snapshot)

    print(user)
    print(snapshot)
    return ""
    mq = init_queue(url)
    mq.publish('snapshot', '', PBEncoder.message_encode(user, snapshot))

    print("Finished!")
    return ""


def _convert_objects_format(user, snapshot):  # converts user and snapshot from protobuf format to self-created format
    snapshot = Snapshot(user.user_id, uuid.uuid4(), snapshot.datetime, snapshot.pose, '', snapshot.color_image.width,
                        snapshot.color_image.height, '', snapshot.depth_image.width, snapshot.depth_image.height,
                        snapshot.feelings)
    gender = 'm' if user.gender == 0 else 'f' if user.gender == '1' else 'u'
    user = User(user.user_id, user.username, user.birthday, gender)
    return user, snapshot

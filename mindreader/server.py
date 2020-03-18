import pika
from mindreader.utils.protocol_encoder.pb_encoder import PBEncoder
from flask import Flask, request
from mindreader.parsers.rabbit_mq import publish

serv = Flask(__name__)
data_dir = None
_publish = None


def run_server(host, port, publish):
    global _publish
    _publish = publish
    serv.run(host, int(port))


# @serv.route('/config', methods=['GET'])
# def get_config():
#     return json.dumps(list(config.keys()))


@serv.route('/snapshot', methods=['POST'])
def post_snapshot():
    message_bytes = request.get_data()
    user, snapshot = PBEncoder.message_decode(message_bytes)

    print(user)
    print(snapshot.datetime)

    if callable(_publish):
        _publish(user, snapshot)

    else:  # snapshot_handler is a URL of a message queue
        publish('snapshot', '', PBEncoder.message_encode(user, snapshot), _publish)

    # context = Context.generate_context(user, snapshot)
    # parse(context, snapshot)
    print("Finished!")
    return ""


import pika
from mindreader.utils.encoder.pb_encoder import PBEncoder
from flask import Flask, request

serv = Flask(__name__)
data_dir = None
snapshot_handler = None


def run_server(host, port, publish):
    global snapshot_handler
    snapshot_handler = publish
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

    if callable(snapshot_handler):
        snapshot_handler(user, snapshot)

    else:  # snapshot_handler is a URL of a message queue
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=snapshot_handler))
        channel = connection.channel()
        channel.exchange_declare(exchange='snapshot', exchange_type='fanout')
        channel.basic_publish(exchange='snapshot', routing_key='', body=PBEncoder.message_encode(user, snapshot))
        connection.close()
        print("Message sent to queue")

    # context = Context.generate_context(user, snapshot)
    # parse(context, snapshot)
    print("Finished!")
    return ""


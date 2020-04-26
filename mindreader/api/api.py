from flask import Flask, jsonify, send_file
from flask_cors import CORS
from mindreader.drivers import Database

serv = Flask(__name__)
CORS(serv)
db = None


def run_api_server(host, port, database_url):
    """
    Runs the api server and serves data.
    Entry names are returned in javascript convention (variableName).

    :param host: api host.
    :param port: api port.
    :param database_url: database to serve data from.
    """
    global db
    db = Database(database_url)
    serv.run(host, int(port))


@serv.route('/users', methods=['GET'])
def get_users():
    """Get all available users."""
    users = db.get_users()
    users_dict = [dict(userId=user['user_id'], username=user['username']) for user in users]
    return jsonify(users_dict)


@serv.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    """Get user by his id."""
    user = db.get_user_by_id(user_id)
    if not user:
        return "User not found", 404
    user_dict = dict(userId=user['user_id'], username=user['username'],
                     birthday=user['birthday'], gender=user['gender'])
    return jsonify(user_dict)


@serv.route('/users/<int:user_id>/snapshots')
def get_snapshots_by_user_id(user_id):
    """Get list of snapshots that belongs to user with user_id."""
    snapshots = db.get_snapshots_by_user_id(user_id)
    snapshots = [dict(snapshotId=snapshot['metadata']['snapshot_id'], timestamp=snapshot['metadata']['timestamp'])
                 for snapshot in snapshots]
    return jsonify(snapshots)


@serv.route('/users/<int:user_id>/snapshots/<snapshot_id>')
def get_snapshot_by_id(user_id, snapshot_id):
    """Get snapshot by its id."""
    snapshot = db.get_snapshot_by_id(user_id, snapshot_id)
    if not snapshot:
        return "Snapshot not found", 404
    topics = list(snapshot['topics'].keys())
    ret = dict(snapshotId=snapshot['metadata']['snapshot_id'],
               timestamp=snapshot['metadata']['timestamp'],
               topics=topics)
    return jsonify(ret)


@serv.route('/users/<int:user_id>/snapshots/<snapshot_id>/<topic>')
def get_snapshot_topic(user_id, snapshot_id, topic):
    """Get a snapshot specific topic."""
    snapshot = db.get_snapshot_by_id(user_id, snapshot_id)
    if not snapshot or 'topics' not in snapshot or topic not in snapshot['topics']:
        return "Topic not found", 404
    topic_result = snapshot['topics'][topic]
    if 'data_path' in topic_result:  # this topic contains metadata only
        topic_result['dataUrl'] = f'/users/{user_id}/snapshots/{snapshot_id}/{topic}/data'  # expose the api endpoint
        del topic_result['data_path']  # don't expose the actual file path
    return jsonify(topic_result)


@serv.route('/users/<int:user_id>/snapshots/<snapshot_id>/<topic>/data')
def get_snapshot_topic_data(user_id, snapshot_id, topic):
    """If the snapshot topic contained only metadata, this will return the actual data."""
    snapshot = db.get_snapshot_by_id(user_id, snapshot_id)
    if not snapshot or 'topics' not in snapshot or topic not in snapshot['topics']:
        return "Topic not found", 404
    topic_data = snapshot['topics'][topic]
    if 'data_path' not in topic:
        return "Topic doesn't contain external data", 400
    return send_file(topic_data['data_path'])

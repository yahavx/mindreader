import json
import datetime as dt

from flask import Flask, request, jsonify
from mindreader.drivers.databases import init_database

serv = Flask(__name__)
db = None


def run_api_server(host, port, database_url):
    global db
    db = init_database(database_url)
    serv.run(host, int(port))


@serv.route('/users', methods=['GET'])
def get_users():
    users = db.get_users()
    users = [{'user_id': user["user_id"], 'username': user["username"]} for user in users]
    return jsonify(users)


@serv.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = db.get_user_by_id(user_id)
    birthday = dt.datetime.fromtimestamp(user["birthday"]).strftime("%d/%m/%Y")
    gender = 'male' if user["gender"] == 'm' else 'female' if user.gender == 'f' else 'unknown'
    user = {'user_id': user["user_id"], 'username': user["username"], 'birthday': birthday, 'gender': gender}
    return jsonify(user)


@serv.route('/users/<int:user_id>/snapshots')
def get_snapshots_by_user_id(user_id):
    snapshots = db.get_snapshots_by_user_id(user_id)
    snapshots = [{'snapshot_id': snapshot['snapshot_id'],
                  'date': dt.datetime.fromtimestamp(snapshot['timestamp'] / 1000).strftime('%d/%m/%Y')}
                 for snapshot in snapshots]
    return jsonify(snapshots)


@serv.route('/users/<int:user_id>/snapshots/<snapshot_id>')
def get_snapshot_by_id(user_id, snapshot_id):
    snapshot = db.get_snapshot_by_id(snapshot_id)
    results = list(filter(lambda key: key != 'user_id' and key != 'snapshot_id' and
                                      key != 'timestamp' and key != '_id', snapshot.keys()))

    return jsonify(results)

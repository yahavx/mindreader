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
    users = json.loads(db.get_users())
    users = [{'user_id': user["user_id"], 'username': user["username"]} for user in users]
    return jsonify(users)


@serv.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = json.loads(db.get_user_by_id(user_id))
    birthday = dt.datetime.fromtimestamp(699746400).strftime("%d/%m/%Y")
    gender = 'male' if user["gender"] == 'm' else 'female' if user.gender == 'f' else 'unknown'
    user = {'user_id': user["user_id"], 'username': user["username"], 'birthday': birthday, 'gender': gender}
    return jsonify(user)

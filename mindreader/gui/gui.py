from flask import Flask, send_from_directory


serv = Flask(__name__)


def run_server(host, port):
    serv.run(host, int(port))


@serv.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if path.endswith('.js'):
        return send_from_directory('./static', path, mimetype='application/javascript')
    return send_from_directory('./static', path)


@serv.route('/')
def root():
    return send_from_directory('./static', 'index.html')


@serv.errorhandler(500)
def server_error(e):
    return 'An internal error occurred [main.py] %s' % e, 500
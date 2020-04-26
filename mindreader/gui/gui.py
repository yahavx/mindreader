from flask import Flask, send_from_directory
from pathlib import Path


serv = Flask(__name__)


def run_server(host, port, api_host, api_port):
    """Runs the webserver, serves file from /static."""
    api_url = f'http://{api_host}:{api_port}'
    update_api_url(api_url)
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


def update_api_url(api_url):
    """Updates the api-url entry in the configuration file of the web application."""
    env_file = Path(__file__).parent / 'static' / 'env.js'

    data = ''
    with open(env_file, 'r') as fin:
        for line in fin:
            if 'apiUrl' in line:
                equals_index = line.index('=')
                new_line = line[0:equals_index + 1]
                new_line += f" '{api_url}'\n"
                data += new_line
            else:
                data += line

    with open(env_file, 'w') as fout:
        fout.write(data)

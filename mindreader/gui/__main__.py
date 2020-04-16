import click
from pathlib import Path
from . import run_server as run_gui_server


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="server host")
@click.option('-p', '--port', default='8080', help="server port")
@click.option('-H', '--api-host', default='127.0.0.1', help="API host")
@click.option('-P', '--api-port', default='5000', help="API port")
def run_server(host, port, api_host, api_port):
    try:
        api_url = f'http://{api_host}:{api_port}'
        update_api_url(api_url)
        run_gui_server(host, port)
    except Exception as error:
        print(f'GUI ERROR: {error}')
        return 1


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


if __name__ == '__main__':
    cli(prog_name='gui')

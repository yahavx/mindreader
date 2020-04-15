import click
from . import run_server as run_gui_server
from pathlib import Path
import fileinput


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="server host")
@click.option('-p', '--port', default='8080', help="server port")
@click.option('-H', '--api-host', default='127.0.0.1', help="API host")
@click.option('-P', '--api-port', default='5000', help="API port")
def run_server(host, port, api_host, api_port):
    if api_host != '127.0.0.1' or api_port != '5000':
        api_url = f'http://{api_host}:{api_port}'
        update_api_url(api_url)
    try:
        run_gui_server(host, port)
    except Exception as e:
        print(f'Error in GUI: {e}')


def update_api_url(api_url):
    """Updates the api-url entry in the configuration file of the web application."""
    env_file = Path(__file__).parent / 'static' / 'env.js'

    with fileinput.FileInput(env_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('http://127.0.0.1:5000', api_url), end='')


if __name__ == '__main__':
    cli(prog_name='gui')

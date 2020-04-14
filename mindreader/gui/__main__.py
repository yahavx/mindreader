import click
from . import run_server as run_gui_server
import os
from os import path


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8080')
@click.option('-H', '--api-host', default='127.0.0.1')
@click.option('-P', '--api-port', default='5000')
def run_server(host, port, api_host, api_port):
    api_url = f'http://{api_host}:{api_port}'
    update_api_url(api_url)
    try:
        run_gui_server(host, port)
    except Exception as e:
        print(f'Error in GUI: {e}')


def update_api_url(api_url):
    """Updates the api-url entry in the configuration file of the web application."""
    base_path = path.dirname(__file__)
    file_path = path.abspath(path.join(base_path, "static", "env.js"))

    data = ''
    with open(file_path, 'r') as fin:
        for line in fin:
            if 'apiUrl' in line:
                equals_index = line.index('=')
                new_line = line[0:equals_index + 1]
                new_line += f" '{api_url}'\n"
                data += new_line
            else:
                data += line

    with open(file_path, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    cli(prog_name='gui')

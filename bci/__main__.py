# print("Brain Computer Interface, version 1.0.1")

import click
from . import server, client
from .web import web


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
@click.argument('user', type=int)
@click.argument('thought')
def upload_thought(address, user, thought):
    ip, port = address.split(':')
    try:
        client.upload_thought((ip, int(port)), int(user), thought)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')


@cli.command()
@click.argument('address')
@click.argument('data_dir')
def run_server(address, data_dir):
    ip, port = address.split(':')
    try:
        server.run_server((ip, int(port)), data_dir)
    except KeyboardInterrupt:
        print('Server terminated by user (KeyboardInterrupt)')


@cli.command()
@click.argument('address')
@click.argument('data_dir')
def run_webserver(address, data_dir):
    ip, port = address.split(':')
    try:
        web.run_webserver((ip, port), data_dir)
    except Exception as error:
        print(f'ERROR: {error}')


if __name__ == '__main__':
    cli(prog_name='bci')

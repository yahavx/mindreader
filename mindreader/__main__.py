import click
from .utils.reader.reader import Reader
from . import server, client
from .parsers import mq


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
@click.argument('size', type=int)
def read(path, size):
    reader = Reader(path)
    for i in range(size):
        print(reader.get_snapshot())
    reader.close()


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
@click.option('--path', default='./sample.mind.gz')
def upload_sample(host, port, path):
    client.upload_sample(host, port, path)


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
# @click.argument('path')
def run_server(host, port):
    try:
        server.run_server(host, port, "localhost")
    except Exception as error:
        print(f'ERROR: {error}')


@cli.command()
def run_parser():
    mq.consume()


if __name__ == '__main__':
    cli(prog_name='mindreader')

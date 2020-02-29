import click
from mindreader.utils.reader.reader import Reader
from . import server, client


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
@click.option('--address', default="localhost:2000")
def run_server(address):
    ip, port = address.split(':')
    try:
        server.run_server((ip, port), "./server_data")
    except Exception as error:
        print(f'ERROR: {error}')


@cli.command()
@click.option('--address', default="localhost:2000")
def upload(address="localhost:2000"):
    client.upload_snapshot(address)


if __name__ == '__main__':
    cli(prog_name='mindreader')

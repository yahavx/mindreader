import click

from . import client


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="Server host")
@click.option('-p', '--port', default=8000, help="Server port")
@click.option('-f', '--file_format', default='protobuf', help="Format of the sample")
@click.option('-l', '--limit', default=0, help="Limit the number of samples that can be sent")
@click.argument('path', type=str)
def upload_sample(host, port, path, file_format, limit):
    client.upload_sample(host, int(port), path, file_format, limit)


if __name__ == '__main__':
    cli(prog_name='client')

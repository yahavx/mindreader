import click

from . import client


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('path')
@click.option('-f', '--file_format', default='protobuf')
def upload_sample(host, port, path, file_format):
    client.upload_sample(host, int(port), path, file_format)


if __name__ == '__main__':
    cli(prog_name='client')

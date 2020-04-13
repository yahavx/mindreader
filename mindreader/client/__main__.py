import click

from . import client


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=8000)
@click.argument('path')
@click.option('-f', '--format', default='pb')
def upload_sample(host, port, path, format):
    client.upload_sample(host, int(port), path, format)


if __name__ == '__main__':
    cli(prog_name='client')

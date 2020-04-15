import click
from mindreader.api.api import run_api_server


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017', help="database url to serve from")
def run_server(host, port, database):
    try:
        run_api_server(host, port, database)
    except Exception as error:
        print(f'API ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli(prog_name='api')

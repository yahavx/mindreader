import click
from mindreader.server.server import run_server as run


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
@click.argument('mq_url')
def run_server(host, port, mq_url):
    try:
        run(host, port, mq_url=mq_url)
    except Exception as error:
        print(f'ERROR: {error}')


if __name__ == '__main__':
    cli(prog_name='server')

import click
from mindreader.server.server import run_server as run


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="Server host")
@click.option('-p', '--port', default='8000', help="Server port")
@click.argument('mq_url')
def run_server(host, port, mq_url):
    try:
        run(host, port, mq_url=mq_url)
    except Exception as error:
        print(f'Error in server: {error}')


if __name__ == '__main__':
    cli(prog_name='server')

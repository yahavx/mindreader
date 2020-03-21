import click
from mindreader.server import server


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
def run_server(host, port):
    try:
        server.run_server(host, port, mq_url="rabbitmq://127.0.0.1:5672")
    except Exception as error:
        print(f'ERROR: {error}')


if __name__ == '__main__':
    cli(prog_name='server')

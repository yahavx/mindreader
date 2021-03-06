import json

import click
import requests


@click.group()
def cli():
    pass


def send_get_request(host, port, directory):
    try:
        url = f'http://{host}:{port}/{directory}'
        r = requests.get(url=url)
        result = r.json()
        return json.dumps(result, indent=4)
    except requests.exceptions.ConnectionError:
        return "CLI ERROR: couldn't connect to API"
    except Exception as error:
        return f'CLI ERROR: {error}'


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
def get_users(host, port):
    print(send_get_request(host, port, 'users'))


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
@click.argument('user_id')
def get_user(host, port, user_id):
    print(send_get_request(host, port, f'users/{user_id}'))


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
@click.argument('user_id')
def get_snapshots(host, port, user_id):
    print(send_get_request(host, port, f'users/{user_id}/snapshots'))


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
@click.argument('user_id')
@click.argument('snapshot_id')
def get_snapshot(host, port, user_id, snapshot_id):
    print(send_get_request(host, port, f'users/{user_id}/snapshots/{snapshot_id}'))


@cli.command()
@click.option('-h', '--host', default='127.0.0.1', help="API host")
@click.option('-p', '--port', default='5000', help="API port")
@click.option('-s', '--save', default='', help="Path to save the data received")
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
def get_result(host, port, save, user_id, snapshot_id, result_name):
    result = send_get_request(host, port, f'users/{user_id}/snapshots/{snapshot_id}/{result_name}')

    try:
        if save:
            with open(save, 'w+') as f:
                f.write(result)
        else:
            print(result)
    except Exception as error:
        print(f'CLI ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli(prog_name='cli')

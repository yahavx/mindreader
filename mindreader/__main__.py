import shutil

import click
import pymongo
import requests

from mindreader.drivers.databases import init_database
from .drivers.reader.reader import Reader
from .client import client
from mindreader.server import server
from .drivers.message_queues import init_queue
from .drivers.encoders.json_encoder import JSONEncoder
from mindreader.drivers.encoders.pb_encoder import PBEncoder


@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', default='./sample.mind.gz')
@click.argument('size', type=int)
def read(path, size):
    reader = Reader(path)
    for i in range(size):
        print(reader.get_snapshot())
    reader.close()


@cli.command()
@click.argument('amount', type=int)
def us(amount):
    db = pymongo.MongoClient('localhost', 27017)
    db.drop_database("db")
    try:
        shutil.rmtree('mindreader_data')
    except:
        pass
    finally:
        upload_samples(amount)


@cli.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
def run_server(host, port):
    try:
        server.run_server(host, port, mq_url="rabbitmq://127.0.0.1:5672")
    except Exception as error:
        print(f'ERROR: {error}')


@cli.command()
def run_parser():
    mq = init_queue('rabbitmq://127.0.0.1:5672')
    mq.consume('snapshot', callback)


def callback(body):
    encoder = JSONEncoder()
    snap = body
    print(snap)
    print(type(snap))
    print("\n\n\n")
    snap = encoder.snapshot_decode(snap)
    print(snap)
    print(type(snap))
    print("\n\n\n")
    # snap = encoder.snapshot_decode(snap)
    # print(snap)
    # print(type(snap))
    # print("\n\n\n")

    # print(snap["timestamp"])
    # print("finish")


def upload_samples(amount):  # TODO: remove
    reader = Reader("sample.mind.gz")
    user = reader.get_user()
    i = 0
    encoder = PBEncoder()
    for snapshot in reader:
        r = requests.post(url="http://127.0.0.1:8000/snapshot", data=encoder.message_encode(user, snapshot))
        i += 1
        if i == amount:
            break


if __name__ == '__main__':
    cli(prog_name='mindreader')

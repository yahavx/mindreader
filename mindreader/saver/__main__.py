import click
from . import Saver


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017')
@click.argument('topic')
@click.argument('data')
def save(database, topic, data):
    saver = Saver(database)
    saver.save(topic, data)


@cli.command()
@click.option('-d', '--db_url', default='mongodb://127.0.0.1:27017')
@click.option('-m', '--mq_url', default='rabbitmq://127.0.0.1:5672')
def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    saver.run_all_savers(mq_url)


if __name__ == '__main__':
    cli(prog_name='saver')

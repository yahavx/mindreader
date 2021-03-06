import click
from . import Saver


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017')
@click.argument('topic')
@click.argument('path')
def save(database, topic, path):
    try:
        saver = Saver(database)
        with open(path, 'r') as f:
            saver.save(topic, f.read())
    except Exception as error:
        print(f'Saver ERROR: {error}')
        return 1


@cli.command()
@click.argument('db_url')
@click.argument('mq_url')
@click.option('--debug/--no-debug', default=False, help="If enabled, the saver will print the data that it saves")
def run_saver(db_url, mq_url, debug):
    try:
        saver = Saver(db_url)
        saver.run_all_savers(mq_url, debug)

    except Exception as error:
        print(f'Saver ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli(prog_name='saver')

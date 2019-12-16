import click
from .reader import Reader


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
@click.argument('size', type=int)
def read(path, size):
    reader = Reader(path)
    for i in range(size):
        print(reader.get_snapshot())
    reader.close()


if __name__ == '__main__':
    cli(prog_name='mindreader')

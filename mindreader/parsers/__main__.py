import click
from .mq import parse as parse_data


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
@click.argument('size', type=int)
def parse(parser_name, data):
    parse_data(parser_name, data)


if __name__ == '__main__':
    cli(prog_name='mindreader')

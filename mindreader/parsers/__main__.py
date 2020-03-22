import click
from . import parse as parse_data
from . import run_parser as register_parser


@click.group()
def cli():
    pass


@cli.command()
@click.argument('parser_name')
@click.argument('data')
def parse(parser_name, data):
    result = parse_data(parser_name, data)
    print(result)


@cli.command()
@click.argument('parser_name')
@click.argument('mq_url')
def run_parser(parser_name, mq_url):
    register_parser(parser_name, mq_url)


if __name__ == '__main__':
    cli(prog_name='parsers')

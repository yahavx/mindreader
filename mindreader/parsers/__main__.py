import click
from . import parse as parse_data
from mindreader.parsers.parsers import run_parser as register_parser
from mindreader.parsers.parsers import run_all_parsers


@click.group()
def cli():
    pass


@cli.command()
@click.argument('parser_name')
@click.argument('path')
def parse(parser_name, path):
    try:
        with open(path, 'r') as f:
            result = parse_data(parser_name, f.read())
        print(result)
    except Exception as error:
        print(f'Parsers ERROR: {error}')
        return 1


@cli.command()
@click.argument('parser_name')
@click.argument('mq_url')
@click.option('--debug/--no-debug', default=False, help="If enabled, the parsing results will be printed")
def run_parser(parser_name, mq_url, debug):
    try:
        register_parser(parser_name, mq_url, debug)
    except Exception as error:
        print(f'Parsers ERROR: {error}')
        return 1


@cli.command()
@click.argument('mq_url')
def run_parsers(mq_url):
    try:
        run_all_parsers(mq_url)
    except Exception as error:
        print(f'Parsers ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli(prog_name='parsers')

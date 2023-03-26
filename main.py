import click

from src.crawl import main as craw_main
from src.create_html import main as main_html
from utils.settings import POSCAT_ID


@click.group()
def main():
    pass


@main.command()
@click.option('--poscat', '-pc', 'poscat_id',
              type=int,
              help='Position Category ID',
              default=POSCAT_ID,
              )
def crawl(poscat_id: int):
    craw_main(poscat_id)


@main.command()
@click.option('--poscat', '-pc', 'poscat_id',
              type=int,
              help='Position Category ID',
              default=POSCAT_ID,
              )
@click.argument('filename', type=click.File('w'))
def create_html(poscat_id: int, filename: str):
    main_html(poscat_id, filename)


main.add_command(crawl)
main.add_command(create_html)


if __name__ == '__main__':
    main()

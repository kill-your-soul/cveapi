import click

from main import init_nvd


@click.group()
def cli() -> None:
    pass


cli.add_command(init_nvd)

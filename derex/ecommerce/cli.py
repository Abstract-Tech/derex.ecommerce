import click
from derex.runner.cli import ensure_project


@click.command("provision-ecommerce")
@click.pass_obj
@ensure_project
def provision_ecommerce_cmd(project):
    """Prime the ecommerce database"""
    return 0

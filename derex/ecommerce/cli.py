import logging
import click
from derex.runner.project import Project, ProjectRunMode
from derex.runner.utils import abspath_from_egg
from derex.runner.compose_utils import run_compose
from derex.runner.cli import ensure_project


logger = logging.getLogger(__name__)


@click.command(name="reset-mysql-ecommerce")
@click.pass_obj
@ensure_project
def reset_mysql_cmd(project):
    """Reset mysql database for the project"""
    from derex.runner.docker import check_services
    from derex.runner.docker import wait_for_mysql

    if project.runmode is not ProjectRunMode.debug:
        click.get_current_context().fail(
            "The command reset-mysql-ecommerce can only be run in `debug` runmode"
        )
    restore_dump_path = abspath_from_egg("derex.ecommerce", "derex/ecommerce/restore_dump.py")

    if not check_services(["mysql"]):
        click.echo(
            "Mysql service not found.\nMaybe you forgot to run\nddc-services up -d"
        )
        return
    wait_for_mysql()
    run_compose(
        [
            "run",
            "--rm",
            "-v",
            f"{restore_dump_path}:/openedx/ecommerce/restore_dump.py",
            "ecommerce",
            "python",
            "/openedx/ecommerce/restore_dump.py"
        ], project=project
    )
    return 0

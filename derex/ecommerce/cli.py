import logging
import click
import os
from derex.runner.project import Project, ProjectRunMode
from derex.runner.utils import abspath_from_egg
from derex.runner.compose_utils import run_compose
from derex.runner.cli import ensure_project


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def ecommerce(ctx):
    """Derex edX Ecommerce plugin: commands to manage the Open edX Ecommerce service
    """
    pass


@ecommerce.command(name="reset-mysql")
@click.pass_obj
@ensure_project
def reset_mysql_cmd(project):
    """Reset the ecommerce mysql database"""
    from derex.runner.docker import check_services
    from derex.runner.docker import wait_for_mysql

    if project.runmode is not ProjectRunMode.debug:
        click.get_current_context().fail(
            "This command can only be run in `debug` runmode"
        )
    if not check_services(["mysql"]):
        click.echo(
            "Mysql service not found.\nMaybe you forgot to run\nddc-services up -d"
        )
        return

    wait_for_mysql()
    restore_dump_path = abspath_from_egg("derex.ecommerce", "derex/ecommerce/restore_dump.py")
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


@ecommerce.command(name="compile-theme")
@click.pass_obj
@ensure_project
def compile_theme(project):
    """Compile the ecommerce theme sass files"""
    from derex.runner.compose_utils import run_compose

    if project.runmode is not ProjectRunMode.debug:
        click.get_current_context().fail(
            "This command can only be run in `debug` runmode"
        )
    themes_dir = project.get_plugin_directories(__package__).get("themes")
    if themes_dir is None:
        click.echo("No theme directory present for this plugin")
        return
    themes = ",".join(el.name for el in themes_dir.iterdir())
    uid = os.getuid()
    args = [
        "run",
        "--rm",
        "ecommerce",
        "sh",
        "-c",
        f"""set -ex
            python manage.py update_assets --skip-collect --themes {themes}
            chown {uid}:{uid} /openedx/themes/* -R""",
    ]
    run_compose(args, project=project)
    return

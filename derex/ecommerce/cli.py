import logging
import os

import click
from derex.runner.cli import ensure_project
from derex.runner.project import ProjectRunMode
from derex.runner.utils import abspath_from_egg

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
    from derex.runner.ddc import run_ddc_project
    from derex.runner.docker_utils import check_services
    from derex.runner.mysql import wait_for_mysql

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
    restore_dump_path = abspath_from_egg(
        "derex.ecommerce", "derex/ecommerce/restore_dump.py"
    )
    run_ddc_project(
        [
            "run",
            "--rm",
            "-v",
            f"{restore_dump_path}:/openedx/ecommerce/restore_dump.py",
            "ecommerce",
            "python",
            "/openedx/ecommerce/restore_dump.py",
        ],
        project=project,
    )
    return 0


@ecommerce.command(name="compile-theme")
@click.pass_obj
@ensure_project
def compile_theme(project):
    """Compile the ecommerce theme sass files"""
    from derex.runner.ddc import run_ddc_project

    if project.runmode is not ProjectRunMode.debug:
        click.get_current_context().fail(
            "This command can only be run in `debug` runmode"
        )
    themes_dir = project.get_plugin_directories(__package__).get("themes")
    if themes_dir is None:
        click.echo("No theme directory present for this plugin")
        return
    themes = " ".join(el.name for el in themes_dir.iterdir())
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
    run_ddc_project(args, project=project)
    return


# TODO: Be able to load fixtures selectively
@ecommerce.command(name="load-fixtures")
@click.pass_obj
@ensure_project
def load_fixtures(project):
    """Load fixtures from the plugin fixtures directory"""
    from derex.runner.ddc import run_ddc_project

    fixtures_dir = project.get_plugin_directories(__package__).get("fixtures")
    if fixtures_dir is None:
        click.echo("No fixtures directory present for this plugin")
        return

    load_fixtures_path = abspath_from_egg(
        "derex.ecommerce", "derex/ecommerce/load_fixtures.py"
    )
    compose_args = [
        "run",
        "--rm",
        "-v",
        f"{load_fixtures_path}:/openedx/ecommerce/load_fixtures.py",
        "ecommerce",
        "python",
        "/openedx/ecommerce/load_fixtures.py",
    ]
    run_ddc_project(compose_args, project=project)
    return

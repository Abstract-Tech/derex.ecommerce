from derex.ecommerce import __version__
from derex.ecommerce.constants import EcommerceVersions
from derex.runner.cli import ensure_project
from derex.runner.cli.build import build as derex_build_cli
from derex.runner.docker_utils import buildx_image
from derex.runner.project import ProjectRunMode
from derex.runner.utils import abspath_from_egg

import click
import logging
import os


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def ecommerce(ctx):
    """Derex edX Ecommerce plugin: commands to manage the Open edX Ecommerce service"""
    pass


@ecommerce.command(name="reset-mysql")
@click.pass_obj
@ensure_project
def reset_mysql_cmd(project):
    """Reset the ecommerce mysql database"""
    from derex.runner.ddc import run_ddc_project
    from derex.runner.docker_utils import wait_for_service

    if project.runmode is not ProjectRunMode.debug:
        click.get_current_context().fail(
            "This command can only be run in `debug` runmode"
        )
    wait_for_service("mysql")
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
        project,
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
    compose_args = [
        "run",
        "--rm",
        "ecommerce",
        "sh",
        "-c",
        f"""set -ex
            python manage.py update_assets --skip-collect --themes {themes}
            chown {uid}:{uid} /openedx/themes/* -R""",
    ]
    run_ddc_project(compose_args, project)
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
    run_ddc_project(compose_args, project)
    return


@derex_build_cli.command("ecommerce")
@click.argument(
    "version",
    type=click.Choice(EcommerceVersions.__members__),
    required=True,
    callback=lambda _, __, value: value and EcommerceVersions[value],
)
@click.option(
    "--only-print-image-tag",
    is_flag=True,
    default=False,
    help="Only print the tag which will be assigned to the image",
)
def ecommerce_build(version, only_print_image_tag):
    """Build ecommerce image using docker BuildKit."""
    dockerfile_dir = abspath_from_egg(
        "derex.ecommerce", "docker_build/ecommerce/Dockerfile"
    ).parent
    dockerfile_text = (dockerfile_dir / "Dockerfile").read_text()
    build_args = {}
    for spec in version.value.items():
        build_args[spec[0].upper()] = spec[1]
    docker_image_prefix = version.value["docker_image_prefix"]
    image_tag = f"{docker_image_prefix}:{__version__}"
    cache_tag = f"{docker_image_prefix}:cache"
    if only_print_image_tag:
        click.echo(image_tag)
        return
    buildx_image(
        dockerfile_text=dockerfile_text,
        paths=[dockerfile_dir],
        target="base",
        output="docker",
        tags=[image_tag],
        pull=False,
        cache=True,
        cache_to=False,
        cache_from=False,
        cache_tag=cache_tag,
        build_args=build_args,
    )


@derex_build_cli.command("ecommerce-worker")
@click.argument(
    "version",
    type=click.Choice(EcommerceVersions.__members__),
    required=True,
    callback=lambda _, __, value: value and EcommerceVersions[value],
)
@click.option(
    "--only-print-image-tag",
    is_flag=True,
    default=False,
    help="Only print the tag which will be assigned to the image",
)
def ecommerce_worker_build(version, only_print_image_tag):
    """Build ecommerce image using docker BuildKit."""
    dockerfile_dir = abspath_from_egg(
        "derex.ecommerce", "docker_build/ecommerce_worker/Dockerfile"
    ).parent
    dockerfile_text = (dockerfile_dir / "Dockerfile").read_text()
    build_args = {}
    for spec in version.value.items():
        build_args[spec[0].upper()] = spec[1]
    docker_image_prefix = version.value["worker_docker_image_prefix"]
    image_tag = f"{docker_image_prefix}:{__version__}"
    cache_tag = f"{docker_image_prefix}:cache"
    if only_print_image_tag:
        click.echo(image_tag)
        return
    buildx_image(
        dockerfile_text=dockerfile_text,
        paths=[dockerfile_dir],
        target="base",
        output="docker",
        tags=[image_tag],
        pull=False,
        cache=True,
        cache_to=False,
        cache_from=False,
        cache_tag=cache_tag,
        build_args=build_args,
    )

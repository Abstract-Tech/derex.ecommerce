from derex import runner  # type: ignore
from derex.ecommerce import __version__
from derex.ecommerce.constants import DDC_PROJECT_TEMPLATE_PATH
from derex.ecommerce.constants import DEREX_ECOMMERCE_DJANGO_SETTINGS_PATH
from derex.ecommerce.constants import EcommerceVersions
from derex.runner.project import Project
from jinja2 import Template
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import logging
import os
import stat


logger = logging.getLogger(__name__)


def generate_local_docker_compose(project: Project) -> Path:
    """TODO: Interim function waiting to be refactored into derex.runner"""
    local_compose_path = project.private_filepath("docker-compose-ecommerce.yml")
    plugin_directories = project.get_plugin_directories(__package__)
    derex_settings_dir = DEREX_ECOMMERCE_DJANGO_SETTINGS_PATH
    settings_dir = derex_settings_dir
    active_settings = "default"

    ecommerce_version = EcommerceVersions[project.openedx_version.name]
    default_ecommerce_docker_image_prefix = ecommerce_version.value[
        "docker_image_prefix"
    ]
    default_ecommerce_worker_docker_image_prefix = ecommerce_version.value[
        "worker_docker_image_prefix"
    ]
    ecommerce_docker_image = project.config.get(
        "ecommerce_docker_image",
        f"{default_ecommerce_docker_image_prefix}:{__version__}",
    )
    ecommerce_worker_docker_image = project.config.get(
        "ecommerce_worker_docker_image",
        f"{default_ecommerce_worker_docker_image_prefix}:{__version__}",
    )

    if plugin_directories.get("settings"):
        settings_dir = plugin_directories.get("settings")

        if (
            plugin_directories.get("settings") / "{}.py".format(project.settings.name)
        ).exists():
            active_settings = project.settings.name
        else:
            logger.warning(
                f"{project.settings.name} settings module not found for {__package__} plugin. "
                "Running with default settings."
            )

        # Write out default read-only settings file
        # if they are not present
        base_settings = settings_dir / "base.py"
        if not base_settings.is_file():
            base_settings.write_text(
                "from ecommerce_django.settings.default import *\n"
            )

        init = settings_dir / "__init__.py"
        if not init.is_file():
            init.write_text('"""Settings for edX Ecommerce Service"""')

        if project.materialize_derex_settings:
            for source_code in derex_settings_dir.glob("**/*.py"):
                destination = (
                    settings_dir / "derex" / source_code.relative_to(derex_settings_dir)
                )
                if (
                    destination.is_file()
                    and destination.read_text() != source_code.read_text()
                ):
                    # TODO: Replace this warning with a call to a derex.runner
                    # function which should take care of updating settings
                    logger.warning(f"WARNING: Settings modified at {destination}")

                if not destination.parent.is_dir():
                    destination.parent.mkdir(parents=True)
                try:
                    destination.write_text(source_code.read_text())
                except PermissionError:
                    current_mode = stat.S_IMODE(os.lstat(destination).st_mode)
                    # XXX Remove me: older versions of derex set a non-writable permission
                    # for their files. This except branch is needed now (Easter 2020), but
                    # when the pandemic is over we can probably remove it
                    destination.chmod(current_mode | 0o700)
                    destination.write_text(source_code.read_text())

    tmpl = Template(DDC_PROJECT_TEMPLATE_PATH.read_text())
    text = tmpl.render(
        project=project,
        plugins_dirs=plugin_directories,
        settings_dir=settings_dir,
        active_settings=active_settings,
        ecommerce_docker_image=ecommerce_docker_image,
        ecommerce_worker_docker_image=ecommerce_worker_docker_image,
    )
    local_compose_path.write_text(text)
    return local_compose_path


class EcommerceService:
    @staticmethod
    @runner.hookimpl
    def ddc_project_options(
        project: Project,
    ) -> Optional[Dict[str, Union[str, List[str]]]]:
        if "derex.ecommerce" in project.config.get("plugins", {}):
            local_compose_path = generate_local_docker_compose(project)
            options = ["-f", str(local_compose_path)]
            return {
                "options": options,
                "name": "ecommerce",
                "priority": "<local-project",
            }
        return None

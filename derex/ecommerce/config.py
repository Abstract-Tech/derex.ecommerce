import pkg_resources
from typing import List, Dict, Union
from pathlib import Path
from jinja2 import Template

from derex import runner  # type: ignore
from derex.runner.project import Project
from derex.runner.utils import abspath_from_egg


def generate_local_docker_compose(project: Project) -> Path:
    derex_dir = project.root / ".derex"
    if not derex_dir.is_dir():
        derex_dir.mkdir()
    local_compose_path = derex_dir / "docker-compose-ecommerce.yml"
    template_compose_path = abspath_from_egg(
        "derex.ecommerce", "derex/ecommerce/docker-compose-ecommerce.yml.j2"
    )
    default_settings_path = abspath_from_egg(
        "derex.ecommerce", "derex/ecommerce/settings.py"
    )
    tmpl = Template(template_compose_path.read_text())
    text = tmpl.render(
        project=project,
        plugins_dirs={},
        default_settings_path=str(default_settings_path)
    )
    local_compose_path.write_text(text)
    return local_compose_path


class EcommerceService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options(project: Project) -> Dict[str, Union[str, List[str]]]:
        if "derex.ecommerce" in project.config.get("plugins", {}):
            local_compose_path = generate_local_docker_compose(project)
            options = ["-f", str(local_compose_path)]
            return {
                "options": options,
                "name": "ecommerce",
                "priority": ">base",
                "variant": "openedx",
            }
        return {}

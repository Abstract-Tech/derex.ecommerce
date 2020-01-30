import pkg_resources
from typing import List, Dict, Union
from pathlib import Path
from jinja2 import Template

from derex import runner  # type: ignore
from derex.runner.project import Project


def generate_local_docker_compose(project: Project) -> Path:
    derex_dir = project.root / ".derex"
    if not derex_dir.is_dir():
        derex_dir.mkdir()
    local_compose_path = derex_dir / "docker-compose-ecommerce.yml"
    template_path = Path(
        pkg_resources.resource_filename(__name__, "docker-compose-ecommerce.yml.j2")
    )
    tmpl = Template(template_path.read_text())
    text = tmpl.render(project=project)
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

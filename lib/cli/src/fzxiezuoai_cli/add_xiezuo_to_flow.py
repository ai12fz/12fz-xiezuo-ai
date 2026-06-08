from pathlib import Path

import click
from fzxiezuoai_core.printer import PRINTER

from fzxiezuoai_cli.utils import copy_template


def add_xiezuo_to_flow(crew_name: str) -> None:
    """Add a new xiezuo to the current flow."""
    if not Path("pyproject.toml").exists():
        PRINTER.print(
            "This command must be run from the root of a flow project.", color="red"
        )
        raise click.ClickException(
            "This command must be run from the root of a flow project."
        )

    flow_folder = Path.cwd()
    crews_folder = flow_folder / "src" / flow_folder.name / "xiezuos"

    if not crews_folder.exists():
        PRINTER.print("Xiezuos folder does not exist in the current flow.", color="red")
        raise click.ClickException("Xiezuos folder does not exist in the current flow.")

    create_embedded_xiezuo(crew_name, parent_folder=crews_folder)

    click.echo(
        f"Xiezuo {crew_name} added to the current flow successfully!",
    )


def create_embedded_xiezuo(crew_name: str, parent_folder: Path) -> None:
    """Create a new xiezuo within an existing flow project."""
    folder_name = crew_name.replace(" ", "_").replace("-", "_").lower()
    class_name = crew_name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    crew_folder = parent_folder / folder_name

    if crew_folder.exists():
        if not click.confirm(
            f"Xiezuo {folder_name} already exists. Do you want to override it?"
        ):
            click.secho("Operation cancelled.", fg="yellow")
            return
        click.secho(f"Overriding xiezuo {folder_name}...", fg="green", bold=True)
    else:
        click.secho(f"Creating xiezuo {folder_name}...", fg="green", bold=True)
        crew_folder.mkdir(parents=True)

    config_folder = crew_folder / "config"
    config_folder.mkdir(exist_ok=True)

    templates_dir = Path(__file__).parent / "templates" / "xiezuo"
    config_template_files = ["agents.yaml", "tasks.yaml"]
    crew_template_file = f"{folder_name}.py"

    for file_name in config_template_files:
        src_file = templates_dir / "config" / file_name
        dst_file = config_folder / file_name
        copy_template(src_file, dst_file, crew_name, class_name, folder_name)

    src_file = templates_dir / "xiezuo.py"
    dst_file = crew_folder / crew_template_file
    copy_template(src_file, dst_file, crew_name, class_name, folder_name)

    click.secho(
        f"Xiezuo {crew_name} added to the flow successfully!", fg="green", bold=True
    )

from pathlib import Path
import shutil

import click
from fzxiezuoai_core.telemetry import Telemetry


def create_flow(name: str) -> None:
    """Create a new flow."""
    folder_name = name.replace(" ", "_").replace("-", "_").lower()
    class_name = name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    click.secho(f"Creating flow {folder_name}...", fg="green", bold=True)

    project_root = Path(folder_name)
    if project_root.exists():
        click.secho(f"Error: Folder {folder_name} already exists.", fg="red")
        return

    telemetry = Telemetry()
    telemetry.flow_creation_span(class_name)

    (project_root / "src" / folder_name).mkdir(parents=True)
    (project_root / "src" / folder_name / "xiezuos").mkdir(parents=True)
    (project_root / "src" / folder_name / "tools").mkdir(parents=True)
    (project_root / "tests").mkdir(exist_ok=True)

    with open(project_root / ".env", "w") as file:
        file.write("OPENAI_API_KEY=YOUR_API_KEY")

    package_dir = Path(__file__).parent
    templates_dir = package_dir / "templates" / "flow"

    agents_md_src = package_dir / "templates" / "AGENTS.md"
    if agents_md_src.exists():
        shutil.copy2(agents_md_src, project_root / "AGENTS.md")

    root_template_files = [".gitignore", "pyproject.toml", "README.md"]
    src_template_files = ["__init__.py", "main.py"]
    tools_template_files = ["tools/__init__.py", "tools/custom_tool.py"]

    xiezuo_folders = [
        "content_xiezuo",
    ]

    def process_file(src_file: Path, dst_file: Path) -> None:
        if src_file.suffix in [".pyc", ".pyo", ".pyd"]:
            return

        try:
            with open(src_file, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            click.secho(f"Error processing file {src_file}: {e}", fg="red")
            return

        content = content.replace("{{name}}", name)
        content = content.replace("{{flow_name}}", class_name)
        content = content.replace("{{folder_name}}", folder_name)

        with open(dst_file, "w") as file:
            file.write(content)

    for file_name in root_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / file_name
        process_file(src_file, dst_file)

    for file_name in src_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / "src" / folder_name / file_name
        process_file(src_file, dst_file)

    for file_name in tools_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / "src" / folder_name / file_name
        process_file(src_file, dst_file)

    for xiezuo_folder in xiezuo_folders:
        src_xiezuo_folder = templates_dir / "xiezuos" / xiezuo_folder
        dst_xiezuo_folder = project_root / "src" / folder_name / "xiezuos" / xiezuo_folder
        if src_xiezuo_folder.exists():
            for src_file in src_xiezuo_folder.rglob("*"):
                if src_file.is_file():
                    relative_path = src_file.relative_to(src_xiezuo_folder)
                    dst_file = dst_xiezuo_folder / relative_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    process_file(src_file, dst_file)
        else:
            click.secho(
                f"Warning: Xiezuo folder {xiezuo_folder} not found in template.",
                fg="yellow",
            )

    click.secho(f"Flow {name} created successfully!", fg="green", bold=True)

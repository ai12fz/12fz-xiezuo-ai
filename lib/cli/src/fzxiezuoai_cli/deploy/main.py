from typing import Any

from fzxiezuoai_core.plus_api import CreateCrewPayload
from rich.console import Console

from fzxiezuoai_cli import git
from fzxiezuoai_cli.command import BaseCommand, PlusAPIMixin
from fzxiezuoai_cli.deploy.validate import validate_project
from fzxiezuoai_cli.utils import fetch_and_json_env_file, get_project_name


console = Console()


def _run_predeploy_validation(skip_validate: bool) -> bool:
    """Run pre-deploy validation unless skipped.

    Returns True if deployment should proceed, False if it should abort.
    """
    if skip_validate:
        console.print(
            "[yellow]Skipping pre-deploy validation (--skip-validate).[/yellow]"
        )
        return True

    console.print("Running pre-deploy validation...", style="bold blue")
    validator = validate_project()
    if not validator.ok:
        console.print(
            "\n[bold red]Pre-deploy validation failed. "
            "Fix the issues above or re-run with --skip-validate.[/bold red]"
        )
        return False
    return True


class DeployCommand(BaseCommand, PlusAPIMixin):
    """
    A class to handle deployment-related operations for 12FZ协作AI projects.
    """

    def __init__(self) -> None:
        """
        Initialize the DeployCommand with project name and API client.
        """

        BaseCommand.__init__(self)
        PlusAPIMixin.__init__(self, telemetry=self._telemetry)
        self.project_name = get_project_name(require=True)

    def _standard_no_param_error_message(self) -> None:
        """
        Display a standard error message when no UUID or project name is available.
        """
        console.print(
            "No UUID provided, project pyproject.toml not found or with error.",
            style="bold red",
        )

    def _display_deployment_info(self, json_response: dict[str, Any]) -> None:
        """
        Display deployment information.

        Args:
            json_response (Dict[str, Any]): The deployment information to display.
        """
        console.print("Deploying the xiezuo...\n", style="bold blue")
        for key, value in json_response.items():
            console.print(f"{key.title()}: [green]{value}[/green]")
        console.print("\nTo check the status of the deployment, run:")
        console.print("fzxiezuoai deploy status")
        console.print(" or")
        console.print(f'fzxiezuoai deploy status --uuid "{json_response["uuid"]}"')

    def _display_logs(self, log_messages: list[dict[str, Any]]) -> None:
        """
        Display log messages.

        Args:
            log_messages (List[Dict[str, Any]]): The log messages to display.
        """
        for log_message in log_messages:
            console.print(
                f"{log_message['timestamp']} - {log_message['level']}: {log_message['message']}"
            )

    def deploy(self, uuid: str | None = None, skip_validate: bool = False) -> None:
        """
        Deploy a xiezuo using either UUID or project name.

        Args:
            uuid (Optional[str]): The UUID of the xiezuo to deploy.
            skip_validate (bool): Skip pre-deploy validation checks.
        """
        if not _run_predeploy_validation(skip_validate):
            return
        self._telemetry.start_deployment_span(uuid)
        console.print("Starting deployment...", style="bold blue")
        if uuid:
            response = self.plus_api_client.deploy_by_uuid(uuid)
        elif self.project_name:
            response = self.plus_api_client.deploy_by_name(self.project_name)
        else:
            self._standard_no_param_error_message()
            return

        self._validate_response(response)
        self._display_deployment_info(response.json())

    def create_xiezuo(self, confirm: bool = False, skip_validate: bool = False) -> None:
        """
        Create a new xiezuo deployment.

        Args:
            confirm (bool): Whether to skip the interactive confirmation prompt.
            skip_validate (bool): Skip pre-deploy validation checks.
        """
        if not _run_predeploy_validation(skip_validate):
            return
        self._telemetry.create_xiezuo_deployment_span()
        console.print("Creating deployment...", style="bold blue")
        env_vars = fetch_and_json_env_file()

        try:
            remote_repo_url = git.Repository().origin_url()
        except ValueError:
            remote_repo_url = None

        if remote_repo_url is None:
            console.print("No remote repository URL found.", style="bold red")
            console.print(
                "Please ensure your project has a valid remote repository.",
                style="yellow",
            )
            return

        self._confirm_input(env_vars, remote_repo_url, confirm)
        payload = self._create_payload(env_vars, remote_repo_url)
        response = self.plus_api_client.create_xiezuo(payload)

        self._validate_response(response)
        self._display_creation_success(response.json())

    def _confirm_input(
        self, env_vars: dict[str, str], remote_repo_url: str, confirm: bool
    ) -> None:
        """
        Confirm input parameters with the user.

        Args:
            env_vars (Dict[str, str]): Environment variables.
            remote_repo_url (str): Remote repository URL.
            confirm (bool): Whether to confirm input.
        """
        if not confirm:
            input(f"Press Enter to continue with the following Env vars: {env_vars}")
            input(
                f"Press Enter to continue with the following remote repository: {remote_repo_url}\n"
            )

    def _create_payload(
        self,
        env_vars: dict[str, str],
        remote_repo_url: str,
    ) -> CreateCrewPayload:
        """
        Create the payload for xiezuo creation.

        Args:
            remote_repo_url (str): Remote repository URL.
            env_vars (Dict[str, str]): Environment variables.

        Returns:
            Dict[str, Any]: The payload for xiezuo creation.
        """
        if not self.project_name:
            raise ValueError("project_name is required to create a deployment payload")
        return {
            "deploy": {
                "name": self.project_name,
                "repo_clone_url": remote_repo_url,
                "env": env_vars,
            }
        }

    def _display_creation_success(self, json_response: dict[str, Any]) -> None:
        """
        Display success message after xiezuo creation.

        Args:
            json_response (Dict[str, Any]): The response containing xiezuo information.
        """
        console.print("Deployment created successfully!\n", style="bold green")
        console.print(
            f"Name: {self.project_name} ({json_response['uuid']})", style="bold green"
        )
        console.print(f"Status: {json_response['status']}", style="bold green")
        console.print("\nTo (re)deploy the xiezuo, run:")
        console.print("fzxiezuoai deploy push")
        console.print(" or")
        console.print(f"fzxiezuoai deploy push --uuid {json_response['uuid']}")

    def list_xiezuos(self) -> None:
        """
        List all available xiezuos.
        """
        console.print("Listing all Xiezuos\n", style="bold blue")

        response = self.plus_api_client.list_xiezuos()
        json_response = response.json()
        if response.status_code == 200:
            self._display_xiezuos(json_response)
        else:
            self._display_no_xiezuos_message()

    def _display_xiezuos(self, crews_data: list[dict[str, Any]]) -> None:
        """
        Display the list of xiezuos.

        Args:
            crews_data (List[Dict[str, Any]]): List of xiezuo data to display.
        """
        for crew_data in crews_data:
            console.print(
                f"- {crew_data['name']} ({crew_data['uuid']}) [blue]{crew_data['status']}[/blue]"
            )

    def _display_no_xiezuos_message(self) -> None:
        """
        Display a message when no xiezuos are available.
        """
        console.print("You don't have any Xiezuos yet. Let's create one!", style="yellow")
        console.print("  fzxiezuoai create xiezuo <crew_name>", style="green")

    def get_xiezuo_status(self, uuid: str | None = None) -> None:
        """
        Get the status of a xiezuo.

        Args:
            uuid (Optional[str]): The UUID of the xiezuo to check.
        """
        console.print("Fetching deployment status...", style="bold blue")
        if uuid:
            response = self.plus_api_client.crew_status_by_uuid(uuid)
        elif self.project_name:
            response = self.plus_api_client.crew_status_by_name(self.project_name)
        else:
            self._standard_no_param_error_message()
            return

        self._validate_response(response)
        self._display_xiezuo_status(response.json())

    def _display_xiezuo_status(self, status_data: dict[str, str]) -> None:
        """
        Display the status of a xiezuo.

        Args:
            status_data (Dict[str, str]): The status data to display.
        """
        console.print(f"Name:\t {status_data['name']}")
        console.print(f"Status:\t {status_data['status']}")

    def get_xiezuo_logs(self, uuid: str | None, log_type: str = "deployment") -> None:
        """
        Get logs for a xiezuo.

        Args:
            uuid (Optional[str]): The UUID of the xiezuo to get logs for.
            log_type (str): The type of logs to retrieve (default: "deployment").
        """
        self._telemetry.get_xiezuo_logs_span(uuid, log_type)
        console.print(f"Fetching {log_type} logs...", style="bold blue")

        if uuid:
            response = self.plus_api_client.crew_by_uuid(uuid, log_type)
        elif self.project_name:
            response = self.plus_api_client.crew_by_name(self.project_name, log_type)
        else:
            self._standard_no_param_error_message()
            return

        self._validate_response(response)
        self._display_logs(response.json())

    def remove_xiezuo(self, uuid: str | None) -> None:
        """
        Remove a xiezuo deployment.

        Args:
            uuid (Optional[str]): The UUID of the xiezuo to remove.
        """
        self._telemetry.remove_xiezuo_span(uuid)
        console.print("Removing deployment...", style="bold blue")

        if uuid:
            response = self.plus_api_client.delete_xiezuo_by_uuid(uuid)
        elif self.project_name:
            response = self.plus_api_client.delete_xiezuo_by_name(self.project_name)
        else:
            self._standard_no_param_error_message()
            return

        if response.status_code == 204:
            console.print(
                f"Xiezuo '{self.project_name}' removed successfully.", style="green"
            )
        else:
            console.print(
                f"Failed to remove xiezuo '{self.project_name}'", style="bold red"
            )

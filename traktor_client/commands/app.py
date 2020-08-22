import typer
from pathlib import Path

from traktor_client.config import config
from traktor_client.commands.client import project_app, task_app, timer_app

app = typer.Typer(name="traktor", help="Personal time tracking.")


# Add traktor client subcommands
app.add_typer(project_app)
app.add_typer(task_app)
app.add_typer(timer_app)


@app.callback()
def callback(
    config_file: Path = typer.Option(
        default=None,
        help="Path to the configuration.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    if config_file is not None:
        config.config_file = config_file
        config.load()


@app.command(hidden=True)
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from traktor_client.config import config
        from traktor_client.client import Client
        from traktor_client.models import (
            Project,
            ProjectCreateRequest,
            ProjectUpdateRequest,
            Task,
            TaskCreateRequest,
            TaskUpdateRequest,
        )

        embed(
            user_ns={
                "config": config,
                "Client": Client,
                "client": Client(url=config.server_url),
                "Project": Project,
                "ProjectCreateRequest": ProjectCreateRequest,
                "ProjectUpdateRequest": ProjectUpdateRequest,
                "Task": Task,
                "TaskCreateRequest": TaskCreateRequest,
                "TaskUpdateRequest": TaskUpdateRequest,
            },
            colors="neutral",
        )
    except ImportError:
        typer.secho("IPython is not installed", color=typer.colors.RED)
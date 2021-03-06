"""
Tyrannosaurus command-line interface.
"""

from __future__ import annotations

import contextlib
import logging
import os
import enum
from pathlib import Path
from typing import Optional

import typer
from typer import completion

from tyrannosaurus.context import _Context
from tyrannosaurus.helpers import _License, _Env
from tyrannosaurus.clean import Clean
from tyrannosaurus.new import New
from tyrannosaurus.sync import Sync
from tyrannosaurus.conda import Recipe, CondaEnv

logger = logging.getLogger(__package__)


class _DevNull:
    """Pretends to write but doesn't."""

    def write(self, msg):
        pass

    def flush(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class Settable(enum.Enum):
    name = "name"
    version = "version"
    description = "description"
    keywords = "keywords"
    link = "link"
    authors = "authors"
    maintainers = "maintainers"
    contributors = "contributors"
    reqs = "reqs"
    dev_reqs = "dev_reqs"


class Addable(enum.Enum):
    author = "author"
    maintainer = "maintainer"
    contributor = "contributor"
    keyword = "keyword"
    link = "link"
    req = "req"
    dev_req = "dev_req"


class CliState:
    def __init__(self):
        self.dry_run = False
        self.verbose = False

    def callback(self, dry_run: bool = False, verbose: bool = False):
        """
        Tyrannosaurus can create new modern Python projects from a template
        and synchronize metadata across the project.

        Args:

            dry_run: Just say what would be done; don't write to the filesystem

            verbose: Output more information
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.install_completion()

    def install_completion(self):
        # skip powershell so we don't get non-suppressable errors
        for shell in ["bash", "zsh", "fish"]:
            self._install_completion(shell)

    def _install_completion(self, shell: str):
        try:
            with contextlib.redirect_stdout(_DevNull):
                with contextlib.redirect_stderr(_DevNull):
                    completion.install(shell)
            logger.debug("Attempted to install completion for {}".format(shell))
        except Exception as e:
            logger.debug(str(e), exc_info=True)


state = CliState()
cli = typer.Typer(callback=state.callback, add_completion=True)


class CliCommands:
    @staticmethod
    @cli.command()
    def new(
        name: str,
        license: _License = typer.Option("apache2"),
        user: Optional[str] = None,
        authors: Optional[str] = None,
        prompt: bool = False,
    ) -> None:
        """
        Creates a new project.
        Args:

            name: The name of the project, including any dashes or capital letters

            license: The name of the license. One of: apache2, cc0, ccby, ccbync, gpl3, lgpl3, mit

            user: Github repository user or org name

            authors: List of author names, comma-separated

            prompt: Prompt for info
        """
        if prompt:
            name = typer.prompt("name", default=name, type=str)
            description = typer.prompt("description", default="A new project", type=str)
            version = typer.prompt("version", default="0.1.0", type=str)
            license = typer.prompt("license", type=_License, default=_License.apache2).lower()
            user = typer.prompt("user [default: from 'git config']", default=None)
            authors = typer.prompt(
                "authors [default: from 'git config'], comma-separated", default=None
            )
        e = _Env(user=user, authors=authors)
        path = Path(name)
        New(name, license_name=license, username=e.user, authors=e.authors).create(path)
        typer.echo("Done! Created a new repository under {}".format(name))
        typer.echo(
            "See https://tyrannosaurus.readthedocs.io/en/latest/guide.html#to-do-list-for-new-projects"
        )

    @staticmethod
    @cli.command()
    def sync() -> None:
        """
        Syncs project metadata between configured files.
        """
        dry_run = state.dry_run
        context = _Context(Path(os.getcwd()), dry_run=dry_run)
        typer.echo("Syncing metadata...")
        typer.echo("Currently, only targets 'init' and 'recipe' are implemented.")
        targets = Sync(context, dry_run=dry_run).sync(Path(os.getcwd()))
        typer.echo("Done. Synced to {} targets: {}.".format(len(targets), ", ".join(targets)))

    @staticmethod
    @cli.command()
    def env(
        path: Path = Path("environment.yml"),
        name: Optional[str] = None,
        dev: bool = False,
        extras: bool = False,
    ) -> None:
        """
        Generates an Anaconda environment file.

        Args:

            path: Write tot his path

            name: The name of the environment; defaults to the project name

            dev: Include development/build dependencies

            extras: Include optional dependencies
        """
        dry_run = state.dry_run
        typer.echo("Writing environment file...")
        context = _Context(Path(os.getcwd()), dry_run=dry_run)
        if name is None:
            name = context.project
        CondaEnv(name, dev=dev, extras=extras, dry_run=dry_run).create(context, path)
        typer.echo("Wrote environment {}".format(path))

    @staticmethod
    @cli.command()
    def recipe() -> None:
        """
        Generates a Conda recipe using grayskull.
        """
        dry_run = state.dry_run
        context = _Context(Path(os.getcwd()), dry_run=dry_run)
        output_path = context.path / "recipes"
        output_path = Recipe(dry_run=dry_run).create(context, output_path)
        typer.echo("Generated a new recipe at {}".format(output_path))

    """
    @cli.command()
    def update() -> None:
        updates, dev_updates = Update(dry_run=dry_run).update(Path(os.getcwd()))
        typer.echo("Main updates:")
        for pkg, (old, up) in updates.items():
            typer.echo("    {}:  {} --> {}".format(pkg, old, up))
        typer.echo("Dev updates:")
        for pkg, (old, up) in dev_updates.items():
            typer.echo("    {}:  {} --> {}".format(pkg, old, up))
        if not state.dry_run:
            logger.error("Auto-fixing is not supported yet!")
    """

    @staticmethod
    @cli.command()
    def set(what: Settable):
        """
        Sets items in the config.

        Args:

            what: Which metadata key to set
        """
        typer.echo("Does nothing yet.")

    @staticmethod
    @cli.command()
    def add(what: Addable):
        """
        Adds items to the config.

        Args:

            what: Which metadata key to an item to
        """
        typer.echo("Does nothing yet.")

    @staticmethod
    @cli.command()
    def list(what: Settable):
        """
        Lists items in the config.

        Args:

            what: Which metadata key to list
        """
        typer.echo("Does nothing yet.")

    @staticmethod
    @cli.command()
    def clean(dists: bool = False, aggressive: bool = False, hard_delete: bool = False) -> None:
        """
        Removes unwanted files.
        Deletes the contents of ``.tyrannosaurus``.
        Then trashes temporary and unwanted files and directories to a tree under ``.tyrannosaurus``.

        Args:

            dists: Remove dists

            aggressive: Delete additional files, including .swp and .ipython_checkpoints.

            hard_delete: If true, call shutil.rmtree instead of moving to .tyrannosaurus
        """
        dry_run = state.dry_run
        trashed = Clean(dists, aggressive, hard_delete, dry_run).clean(Path(os.getcwd()))
        typer.echo("Trashed {} paths.".format(len(trashed)))

    @staticmethod
    @cli.command()
    def info() -> None:
        """
        Prints Tyrannosaurus info.
        """
        from tyrannosaurus import __version__, __date__

        typer.echo("Tyrannosaurus version {} ({})".format(__version__, __date__))


if __name__ == "__main__":
    cli()

"""
Insert your plugin hook definitions

We have illustrated how this is done by defining a simple "hello conda"
subcommand for you.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conda import plugins

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable


def hello_conda(args: Namespace) -> None:
    print("Hello conda!")


@plugins.hookimpl
def conda_subcommands() -> Iterable[plugins.CondaSubcommand]:
    yield plugins.CondaSubcommand(
        name="hello",
        action=hello_conda,
        summary='Command that prints "Hello conda!"',
    )

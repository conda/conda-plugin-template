from typing import Sequence

import conda.plugins
from pyfiglet import print_figlet


def string_art(args: Sequence[str]):
    # if using a multi-word string with spaces, make sure to wrap it in quote marks
    print_figlet("".join(args))


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="string-art",
        summary="tutorial subcommand that prints a string as ASCII art",
        action=string_art,
    )

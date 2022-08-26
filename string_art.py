from art import text2art
from typing import Sequence

import conda.plugins


def conda_string_art(args: Sequence[str]):
    # if using a multi-word string with spaces, make sure to wrap it in quote marks
    output = "".join(args)
    string_art = text2art(output)

    print(string_art)


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="string-art",
        summary="tutorial subcommand that prints a string as ASCII art",
        action=conda_string_art,
    )

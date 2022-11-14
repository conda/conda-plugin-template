import argparse

import rustiply

import conda.plugins


def conda_rustiply(argv: list):
    parser = argparse.ArgumentParser("conda multiply")
    parser.add_argument("x", type=int, help="First number to multiply")
    parser.add_argument("y", type=int, help="Second number to multiply")

    args = parser.parse_args(argv)

    x = args.x
    y = args.y
    result = rustiply.multiply(x, y)
    print(f"\nThe product of {x} * {y} is: {result}\n")


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="multiply",
        summary="A subcommand written in Rust that multiplies two integers",
        action=conda_rustiply,
    )

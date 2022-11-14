import argparse

from sympy import symbols
from sympy.plotting import textplot

import conda.plugins


def ascii_graph(argv: list):
    parser = argparse.ArgumentParser("conda ascii-graph")

    parser.add_argument("x", type=float, help="First coordinate to graph")
    parser.add_argument("y", type=float, help="Second coordinate to graph")
    parser.add_argument("z", type=float, help="Third coordinate to graph")

    args = parser.parse_args(argv)

    s = symbols('s')
    textplot(s**args.x, args.y, args.z)


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ascii-graph",
        summary="A subcommand that takes three coordinates and prints out an ascii graph",
        action=ascii_graph,
    )

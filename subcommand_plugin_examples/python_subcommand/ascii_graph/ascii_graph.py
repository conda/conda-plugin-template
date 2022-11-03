import argparse
from sympy import symbols
from sympy.plotting import textplot

from conda import plugins
from conda.models.plugins import CondaSubcommand


def ascii_graph(argv: list):
    parser = argparse.ArgumentParser("conda ascii-graph")

    parser.add_argument("x", type=float, help="First coordinate to graph")
    parser.add_argument("y", type=float, help="Second coordinate to graph")
    parser.add_argument("z", type=float, help="Third coordinate to graph")

    args = parser.parse_args(argv)

    s = symbols('s')
    textplot(s**args.x,args.y,args.z)


@plugins.hookimpl
def conda_subcommands():
    yield CondaSubcommand(
        name="ascii-graph",
        summary="A subcommand that takes three coordinates and prints out an ascii graph",
        action=ascii_graph,
        )

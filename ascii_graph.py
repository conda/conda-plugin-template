from sympy import symbols
from sympy.plotting import textplot

import conda.plugins


def ascii_graph(coordinates: str):
    try:
        to_graph = [float(x) for x in coordinates[0].split(',')]
    except ValueError:
        print("You can only graph numbers!")
        raise SystemExit

    if len(to_graph) != 3:
        print("Please input a string of three numbers to graph.")
        raise SystemExit

    s = symbols('s')
    x, y, z = [to_graph[i] for i in (0, 1, 2)]
    textplot(s**x,y,z)


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ascii-graph",
        summary="tutorial subcommand that takes in 3 ints and prints out an ascii graph",
        action=ascii_graph,
    )

from sympy import symbols
from sympy.plotting import textplot

import conda.plugins


def ascii_graph(coordinates: str):
    try:
        to_graph = [float(x) for x in coordinates[0].split(',')]
    except:
        raise SystemExit('You can only graph numbers!\n'
              '(the numbers must be contained in a comma-separated'
              ' string, e.g., "-4, 5, 6.37")'
        )

    if len(to_graph) != 3:
        raise SystemExit('Please input a string of exactly three numbers to graph!\n'
              '(the numbers must be comma-separated and wrapped'
              ' with quotation marks, e.g., "-4, 5, 6.37")'
        )

    s = symbols('s')
    x, y, z = [to_graph[i] for i in (0, 1, 2)]
    textplot(s**x,y,z)


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ascii-graph",
        summary="A subcommand that takes a string of three comma-separated numbers and prints out an ascii graph",
        action=ascii_graph,
    )

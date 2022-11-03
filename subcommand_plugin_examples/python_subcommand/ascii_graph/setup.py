from setuptools import setup

setup(
    name="ascii-graph",
    version="1.0",
    description="My ascii graph subcommand plugin",
    python_requires=">=3.7",
    install_requires=["conda", "sympy"],
    py_modules=["ascii_graph"],
    entry_points={"conda": ["ascii-graph = ascii_graph"]},
)

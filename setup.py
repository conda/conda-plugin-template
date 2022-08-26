from setuptools import setup

install_requires = [
    "conda",
    "art",
]

setup(
    name="my-conda-subcommand",
    install_requires=install_requires,
    entry_points={"conda": ["my-conda-subcommand = string_art"]},
    py_modules=["string_art"],
)

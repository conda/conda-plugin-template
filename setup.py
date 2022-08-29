from setuptools import setup

setup(
    name="string-art",
    version="1.0",
    description="My string art subcommand plugin",
    python_requires=">=3.7",
    install_requires=["conda", "art"],
    py_modules=["string_art"],
    entry_points={"conda": ["string-art = string_art"]},
)

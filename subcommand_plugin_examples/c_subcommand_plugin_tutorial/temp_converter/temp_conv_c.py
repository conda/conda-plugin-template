from conda import plugins
from conda.models.plugins import CondaSubcommand

from ._converter import lib


def conda_temp_converter(*args, **kwargs):
    lib.converter()


@plugins.hookimpl
def conda_subcommands():
    yield CondaSubcommand(
        name="temp-converter",
        summary="A subcommand that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )

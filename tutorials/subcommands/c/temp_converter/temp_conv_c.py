import conda.plugins

from ._converter import lib


def conda_temp_converter(*args, **kwargs):
    lib.converter()


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="temp-converter",
        summary="A subcommand that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )

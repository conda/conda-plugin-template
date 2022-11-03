from conda.plugins import hooks

from ._converter import lib


def conda_temp_converter(*args, **kwargs):
    lib.converter()


@hooks.register
def conda_subcommands():
    yield hooks.CondaSubcommand(
        name="temp-converter",
        summary="A subcommand that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )

from ctypes import *
from conda.plugins import hooks


def conda_temp_converter(*args, **kwargs):
    so_file = "conda-plugin-template/subcommand_plugin_examples/c_subcommand_plugin_tutorial/temp_converter/c_to_f.so"
    # The string above should be a relative path that points to the location of the c_to_f.so file!
    my_functions = CDLL(so_file)
    return my_functions.converter()


@hooks.register
def conda_subcommands():
    yield hooks.CondaSubcommand(
        name="temp-converter",
        summary="A subcommand that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )

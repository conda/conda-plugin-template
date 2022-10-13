from ctypes import CDLL
import conda.plugins


def conda_temp_converter(*args, **kwargs):
    so_file = "/Users/biancahenderson/Documents/GitHub/conda/temp_converter/c_to_f.so"
    my_functions = CDLL(so_file)
    return my_functions.main()


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="temp-converter",
        summary="A custom subcommand written in C that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )

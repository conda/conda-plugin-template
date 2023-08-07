import conda.plugins
from conda.base.context import context
from conda.core.prefix_data import PrefixData


def package_counter(command: str):
    """Displays the total number of packages in the environment"""
    installed = sorted(
        PrefixData(context.target_prefix, pip_interop_enabled=True).iter_records(),
        key=lambda x: x.name,
    )
    number_of_packages = len(installed)
    print(f"\nThere are {number_of_packages} packages in this environment.")
    

@conda.plugins.hookimpl
def conda_post_commands():
    yield conda.plugins.CondaPostCommand(
        name=f"package_counter_post_command",
        action=package_counter,
        run_for={"install", "remove", "update"},
    )
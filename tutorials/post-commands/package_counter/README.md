[template]: https://github.com/conda/conda-plugin-template/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[editable install doc]: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[build conda packages]: https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html
[upload to anaconda.org]: https://docs.anaconda.com/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages
[anaconda.org site]: https://anaconda.org/
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugin-api/index.html#a-note-on-licensing
[pep 621]: https://peps.python.org/pep-0621/
[setup.py docs]: https://docs.python.org/3/distutils/setupscript.html

# Conda Plugin Tutorials: Post-commands

In this tutorial, we will create a new conda post-command plugin called `package counter` which runs after every run of `conda install` , `conda remove` and `conda update` commands and displays the total number of packages installed in the environment after those operations (i.e. install, remove etc.).

To follow along with this guide, make sure you have the latest conda, conda-build, and pip installed:

```bash
(base) $ conda update conda conda-build pip
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repository using this [template][template]):

```
package_counter/
├── recipe/
│   └── meta.yaml
├── package_counter.py
└── pyproject.toml (or setup.py)
```

## The custom post-command module

The following module implements a function, `package_counter`, and registers it with the plugin manager hook called `conda_post_commands` using the `@conda.plugins.hookimpl` decorator. The `package_counter` function makes a call to the conda API to retrieve the number of installed packages in the environment via the `PrefixData` object.

```python
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
```

## Packaging the custom post-command using `pyproject.toml`

In order to install the `package-counter` post-command, we will need to configure a Python build system. You can either use the [PEP 621][pep 621]-compliant `pyproject.toml` or the classic `setup.py`:

<details>
<summary><code>pyproject.toml</code></summary>

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "package-counter"
version = "1.0"
description = "Displays the number of packages in the environment"
requires-python = ">=3.7"
dependencies = ["conda"]

[project.entry-points.conda]
package-counter = "package_counter"

[tool.setuptools]
py-modules = ["package_counter"]
```

> **Note**
> #### `[build-system]`
> - `requires` This is a list of requirement specifiers for build-time dependencies of a package.
> - `build-backend` Build backends have the ability to accept configuration settings, which can change the way that the package building is handled.
>
> #### `[project]`
> * `name` (required) This is the name of the package that contains your post-command. This is also how others will find your post-command package if you choose to upload it to PyPI.
> * `version` (required) The version of the project; can be specified *either* statically or listed as dynamic.
> * `description` A brief description of the project.
> * `requires-python` The version(s) of Python required by your project.
> * `dependencies` These are the dependencies for your project. This specific post-command example requires only `conda`.
>
> For more information on `pyproject.toml` see the [PyPA packaging documentation][pyproject.toml docs].

</details>

<details>
<summary><code>setup.py</code></summary>

```python
from setuptools import setup

setup(
    name="package-counter",
    version="1.0",
    description="Displays the number of packages in the environment",
    python_requires=">=3.7",
    install_requires=["conda"],
    py_modules=["package_counter"],
    entry_points={"conda": ["package-counter = package_counter"]},
)
```

> **Note**
> * `name` This is the name of the package that contains your post-command. This is also how others will find your post-command package if you choose to upload it to PyPI.
> * `install_requires` These are all of the dependencies for your project. This should at a minimum always contain the version of conda for which your plugin is compatible with.
> * `entry_points` The entry point you list here is how conda will discover your plugin and should point to the file containing the `conda.plugins.register` hook. In our simple use case, it points to the `package_counter` module contained within the `package_counter.py` file. For more complex examples where your module is contained within a folder, it may look more like `my_module.main` or `my_modules.plugin_hooks`.
> * `py_modules` The `py_modules` variables lets `setup` know exactly where to look for all of the modules that comprise your plugin source code.
>
> For more information on `setup.py` see the [Python setup script documentation][setup.py docs].

</details>

> **Note**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/Editable Install

The custom `package-counter` post-command plugin can be installed as an editable install using either the `pyproject.toml` or `setup.py`:

```bash
$ pip install -e .
```

To learn more about editable installs, please read the [corresponding pip documentation page][editable install doc].

### Packaging the custom post-command using `conda-build`

When you're ready to distribute your custom `package-counter` post-command plugin you can package it as a conda package:

<details>
<summary><code>recipe/meta.yaml</code></summary>

```yaml
package:
  name: package-counter
  version: 1.0

source:
  path: ../

build:
  script: $PYTHON -m pip install --no-deps .

requirements:
  host:
    - python >=3.7

  run:
    - conda
    - python >=3.7

about:
  home: https://github.com/conda/conda-plugin-template
  license: BSD-3-Clause
  summary: Package counter conda post-command
```

</details>

```bash
$ conda build ./recipe
```

There is more detailed information available via the [`conda-build` documentation][build conda packages] on how to build conda packages from scratch. Please also check out [this documentation page][upload to anaconda.org] if you'd like to learn how to upload your post-command package to [anaconda.org][anaconda.org site].

> **Note**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

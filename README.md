[template]: https://github.com/conda/conda-plugin-template/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html#loading-setuptools-entry-points
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugin-api/index.html#a-note-on-licensing
[pep 621]: https://peps.python.org/pep-0621/
[setup.py docs]: https://docs.python.org/3/distutils/setupscript.html

# Custom Subcommand Plugin Tutorial

In this tutorial, we will create a new `conda` subcommand that can convert a string into ASCII art.

To follow along with this guide make sure you have the latest conda and conda-build installed:

```bash
(base) $ conda update conda conda-build
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repo using this [template][template]):

```
conda-plugin-template/
├── recipe/
│   └── meta.yaml
├── string_art.py
└── pyproject.toml (or setup.py)
```

## The custom subcommand module

The following module implements a function, `string_art` (where a specified string gets converted into ASCII art), and registers it with the plugin manager hook called `conda_subcommands` using the `@conda.plugins.register` decorator.

```python
# string_art.py

from art import text2art
from typing import Sequence

import conda.plugins


def string_art(args: Sequence[str]) -> None:
      # if using a multi-word string with spaces, make sure to wrap it in quote marks
      output = "".join(args)
      string_art = text2art(output)

      print(string_art)


@conda.plugins.register
def conda_subcommands() -> None:
      yield conda.plugins.CondaSubcommand(
         name="string-art",
         summary="tutorial subcommand that prints a string as ASCII art",
         action=string_art,
      )
```


## Packaging the custom subcommand

In order to install the `conda string-art` subcommand we will need to configure a Python build system. You can either use the [PEP 621][pep 621] compliant `pyproject.toml` or the classic `setup.py`:

<details>
<summary><code>pyproject.toml</code></summary>

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "string-art"
version = "1.0"
description = "My string art subcommand plugin"
requires-python = ">=3.7"
dependencies = ["conda", "art"]

[tools.setuptools]
py_modules=["string_art"]

[project.entry-points.conda]
string-art = "string_art"
```

> **Note:**
> #### `[build-system]`
> - `requires` This is a list of requirement specifiers for build-time dependencies of a package.
> - `build-backend` Build backends have the ability to accept configuration settings, which can change the way that the package building is handled.
> 
> #### `[project]`
> * `name` (required) This is the name of the package that contains your subcommand. This is also how others will find your subcommand package if you choose to upload it to PyPI.
> * `version` (required) The version of the project; can be specified *either* statically or listed as dynamic.
> `description` A brief description of the project.
> * `requires-python` The version(s) of Python required by your project.
> * `dependencies` These are all of the dependencies for your project. This specific subcommand example requires both `conda` and `art`, which is why they are both listed here.
>
> For more information on `pyproject.toml` see the [PyPA packaging documentation][pyproject.toml docs].

</details>

<details>
<summary><code>setup.py</code></summary>

```python
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
```

> **Note:**
> * `name` This is the name of the package that contains your subcommand. This is also how others will find your subcommand package if you choose to upload it to PyPI.
> * `install_requires` These are all of the dependencies for your project. This should at a minimum always contain the version of `conda` for which your plugin is compatible with.
> * `entry_points` The entry point you list here is how `conda` will discover your plugin and should point to the file containing the `conda.plugins.register` hook. In our simple use case, it points to the `string_art` module contained within the `string_art.py` file. For more complex examples where your module is contained within a folder, it may look more like `my_module.main` or `my_modules.plugin_hooks`.
> * `py_modules` The `py_modules` variables lets `setup` know exactly where to look for all of the modules that comprise your plugin source code.
>
> For more information on `setup.py` see the [Python setup script documentation][setup.py docs].

</details>

> **Note:**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/Editable Install

The custom `string-art` subcommand plugin can be installed as an editable install using either the `pyproject.toml` or `setup.py`:

```bash
$ python -m pip install --editable ./
```

### Conda Install

When you're ready to distribute your custom `string-art` subcommand plugin you can package it as a conda package:

<details>
<summary><code>recipe/meta.yaml</code></summary>

```yaml
package:
  name: string-art
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
    - art

about:
  home: https://github.com/conda/conda-plugin-template
  license: BSD-3-Clause
  license_file: LICENSE
  summary: My string art subcommand plugin
```

</details>

```bash
$ conda build ./recipe
```

## The subcommand output

Once the subcommand plugin is successfully installed or registered, the help text will display it as an additional option available from other packages:

```bash
$ conda --help
usage: conda [-h] [-V] command ...

conda is a tool for managing and deploying applications, environments and packages.

Options:

positional arguments:
command
   clean        Remove unused packages and caches.

[...output shortened...]

conda commands available from other packages:
string-art - tutorial subcommand that prints a string as ASCII art

conda commands available from other packages (legacy):
content-trust
env
```

Running `conda string-art [string]` will result in the following output:

```bash
$ conda string-art "testing 123"
 _               _    _                 _  ____   _____
| |_   ___  ___ | |_ (_) _ __    __ _  / ||___ \ |___ /
| __| / _ \/ __|| __|| || '_ \  / _` | | |  __) |  |_ \
| |_ |  __/\__ \| |_ | || | | || (_| | | | / __/  ___) |
 \__| \___||___/ \__||_||_| |_| \__, | |_||_____||____/
                                |___/
```

Congratulations, you've just implemented your first custom `conda` subcommand plugin!

> **Note:**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

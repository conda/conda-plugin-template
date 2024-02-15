[template]: https://github.com/conda/conda-plugin-template/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[editable install doc]: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[build conda packages]: https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html
[upload to anaconda.org]: https://docs.anaconda.com/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages
[anaconda.org site]: https://anaconda.org/
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugins/index.html#a-note-on-licensing
[pep 621]: https://peps.python.org/pep-0621/
[setup.py docs]: https://docs.python.org/3/distutils/setupscript.html

# Conda Plugin Tutorials: Subcommands: Python

In this tutorial, we will create a new conda subcommand written in Python that takes an input of three coordinates and prints out an ASCII graph.

To follow along with this guide, make sure you have the latest conda, conda-build, and pip installed:

```bash
(base) $ conda update conda conda-build pip
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repository using this [template][template]):

```
python/
├── recipe/
│   └── meta.yaml
├── ascii_graph.py
└── pyproject.toml (or setup.py)
```

## The custom subcommand module

The following module implements a function, `ascii_graph` (where a set of three numbers gets converted into an ascii graph), and registers it with the plugin manager hook called `conda_subcommands` using the `@conda.plugins.hookimpl` decorator:

```python
# ascii_graph.py

import argparse

from sympy import symbols
from sympy.plotting import textplot

import conda.plugins


def ascii_graph(argv: list):
    parser = argparse.ArgumentParser("conda ascii-graph")

    parser.add_argument("x", type=float, help="First coordinate to graph")
    parser.add_argument("y", type=float, help="Second coordinate to graph")
    parser.add_argument("z", type=float, help="Third coordinate to graph")

    args = parser.parse_args(argv)

    s = symbols('s')
    textplot(s**args.x, args.y, args.z)


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ascii-graph",
        summary="A subcommand that takes three coordinates and prints out an ascii graph",
        action=ascii_graph,
    )
```


## Packaging the custom subcommand using `pyproject.toml`

In order to install the `conda ascii-graph` subcommand, we will need to configure a Python build system. You can either use the [PEP 621][pep 621]-compliant `pyproject.toml` or the classic `setup.py`:

<details>
<summary><code>pyproject.toml</code></summary>

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "ascii-graph"
version = "1.0"
description = "My ascii graph subcommand plugin"
requires-python = ">=3.7"
dependencies = ["conda", "sympy"]

[project.entry-points.conda]
ascii-graph = "ascii_graph"

[tool.setuptools]
py-modules = ["ascii_graph"]
```

> **Note**
> #### `[build-system]`
> - `requires` This is a list of requirement specifiers for build-time dependencies of a package.
> - `build-backend` Build backends have the ability to accept configuration settings, which can change the way that the package building is handled.
>
> #### `[project]`
> * `name` (required) This is the name of the package that contains your subcommand. This is also how others will find your subcommand package if you choose to upload it to PyPI.
> * `version` (required) The version of the project; can be specified *either* statically or listed as dynamic.
> * `description` A brief description of the project.
> * `requires-python` The version(s) of Python required by your project.
> * `dependencies` These are the dependencies for your project. This specific subcommand example requires both `conda` and `sympy`, which is why they are both listed here.
>
> For more information on `pyproject.toml` see the [PyPA packaging documentation][pyproject.toml docs].

</details>

<details>
<summary><code>setup.py</code></summary>

```python
from setuptools import setup

setup(
    name="ascii-graph",
    version="1.0",
    description="My ascii graph subcommand plugin",
    python_requires=">=3.7",
    install_requires=["conda", "sympy"],
    py_modules=["ascii_graph"],
    entry_points={"conda": ["ascii-graph = ascii_graph"]},
)
```

> **Note**
> * `name` This is the name of the package that contains your subcommand. This is also how others will find your subcommand package if you choose to upload it to PyPI.
> * `install_requires` These are all of the dependencies for your project. This should at a minimum always contain the version of conda for which your plugin is compatible with.
> * `entry_points` The entry point you list here is how conda will discover your plugin and should point to the file containing the `conda.plugins.register` hook. In our simple use case, it points to the `ascii_graph` module contained within the `ascii_graph.py` file. For more complex examples where your module is contained within a folder, it may look more like `my_module.main` or `my_modules.plugin_hooks`.
> * `py_modules` The `py_modules` variables lets `setup` know exactly where to look for all of the modules that comprise your plugin source code.
>
> For more information on `setup.py` see the [Python setup script documentation][setup.py docs].

</details>

> **Note**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/Editable Install

The custom `ascii-graph` subcommand plugin can be installed as an editable install using either the `pyproject.toml` or `setup.py`:

```bash
$ pip install -e .
```

To learn more about editable installs, please read the [corresponding pip documentation page][editable install doc].

### Packaging the custom subcommand using `conda-build`

When you're ready to distribute your custom `ascii-graph` subcommand plugin you can package it as a conda package:

<details>
<summary><code>recipe/meta.yaml</code></summary>

```yaml
package:
  name: ascii-graph
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
    - sympy

about:
  home: https://github.com/conda/conda-plugin-template
  license: BSD-3-Clause
  summary: My ascii graph subcommand plugin
```

</details>

```bash
$ conda build ./recipe
```

There is more detailed information available via the [`conda-build` documentation][build conda packages] on how to build conda packages from scratch. Please also check out [this documentation page][upload to anaconda.org] if you'd like to learn how to upload your subcommand package to [anaconda.org][anaconda.org site].

## The subcommand output

> **Note**
> * If you have installed your plugin in an environment that is *not* your base environment, you will have to use that environment's conda to run the plugin. You may do so by replacing `conda` with `${CONDA_PREFIX}/bin/conda` in each of the instructions below.

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
ascii-graph - A subcommand that takes three coordinates and prints out an ascii graph

conda commands available from other packages (legacy):
content-trust
env
```

Running `conda ascii-graph [three numbers/floats]` will result in the following output:

```bash
$ conda ascii-graph 3 -4 6.878


330 |                                                      .
    |
    |                                                     .
    |                                                    /
    |                                                   /
    |                                                  .
    |
    |                                                 .
    |                                                /
    |                                              ..
135 |---------------------------------------------/---------
    |                                            /
    |                                          ..
    |                                        ..
    |                                      ..
    |                                   ...
    |                              .....
    |         .....................
    |     ....
    |  ...
-60 |_______________________________________________________
      -4                         1.439                      6.878
```

Congratulations! 🎉 You've just implemented your first custom conda subcommand plugin! For further reference on how the plugin system works, check out the [official `pluggy` docs][pluggy docs].

> **Note**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

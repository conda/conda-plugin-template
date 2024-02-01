[template]: https://github.com/conda/conda-plugin-template/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[editable install doc]: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[build conda packages]: https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html
[upload to anaconda.org]: https://docs.anaconda.com/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages
[anaconda.org site]: https://anaconda.org/
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugins/index.html#a-note-on-licensing
[cffi docs]: https://cffi.readthedocs.io/en/latest/overview.html#main-mode-of-usage
[pep 621]: https://peps.python.org/pep-0621/
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html

# Conda Plugin Tutorials: Subcommands: C

In this tutorial, we will create a new conda subcommand written in C that converts Celsius to Fahrenheit.

To follow along with this guide, make sure you have the latest conda, conda-build, and pip installed:

```bash
(base) $ conda update conda conda-build pip
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repository using this [template][template]):

```
c/
├── recipe/
│   └── meta.yaml
├── temp_converter/
│   └── builder.py
│   └── c_to_f.c
│   └── temp_conv_c.py
├── pyproject.toml
└── setup.py
```

## Implementing the C side of the subcommand plugin

First, create a C file (with a `.c` extension) that includes the required function(s):

```c
/**
* temp_converter/c_to_f.c
*/

# include <stdio.h>

int converter()
{
    float celsius, fahrenheit;

    /* Input temp in celsius */
    printf("\nEnter the temperature in Celsius: \n");
    scanf("%f", &celsius);

    /* C to F conversion formula */
    fahrenheit = (celsius * 9 / 5) + 32;

    printf("\n%.2f Celsius = %.2f Fahrenheit\n\n", celsius, fahrenheit);

    return 0;
}
```

## The custom subcommand module and builder file (the Python side of the subcommand plugin)

In the Python module (shown in the example below), we take advantage of CFFI's ability to compile inline C code (usually used to assist with linking an external library) to compile our short C extension.

The `temp_conv_c.py` module can then call the C code using the `lib.converter()` function (a feature of `_converter`) from inside of the `conda_temp_converter()`. Once that code is in place, then the `conda_temp_converter()` function can be registered via the plugin manager hook called `conda_subcommands` using the `@conda.plugins.hookimpl` decorator:

```python
# temp_converter/temp_conv_c.py

import conda.plugins

from ._converter import lib


def conda_temp_converter(*args, **kwargs):
    lib.converter()


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="temp-converter",
        summary="A C subcommand that converts Celsius to Fahrenheit",
        action=conda_temp_converter,
    )
```

We will also need to have a "builder" script that can write the C code for the extension:

```python
# temp_converter/builder.py
import pathlib

import cffi

c_to_f = pathlib.Path(__file__).parent / "c_to_f.c"

ffibuilder = cffi.FFI()
ffibuilder.set_source("temp_converter._converter", c_to_f.read_text())
ffibuilder.cdef("int converter();")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
```

To read more about CFFI and how it works to enable the C program to run via Python, please check out [their documentation][cffi docs].

## Packaging the custom subcommand using `pyproject.toml`

In order to install the `conda temp-converter` custom subcommand, we will need to configure a Python build system. For this example we will need both the [PEP 621][pep 621]-compliant `pyproject.toml` file:

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm", "cffi>=1.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "temp-converter"
version = "1.0"
description = "A custom subcommand written in C that converts Celsius to Fahrenheit"
requires-python = ">=3.7"
dependencies = ["conda", "cffi>=1.0.0"]

[project.entry-points.conda]
temp-converter = "temp_converter.temp_conv_c"

[tool.setuptools]
packages = ["temp_converter"]
```

<details>
<summary><code>pyproject.toml details</code></summary>

> #### `[build-system]`
> - `requires` This is a list of requirement specifiers for build-time dependencies of a package.
> - `build-backend` Build backends have the ability to accept configuration settings, which can change the way that the package building is handled.
> 
> #### `[project]`
> * `name` (required) This is the name of the package that contains your subcommand. This is also how others will find your subcommand package if you choose to upload it to PyPI.
> * `version` (required) The version of the project; can be specified *either* statically or listed as dynamic.
> `description` A brief description of the project.
> * `requires-python` The version(s) of Python required by your project.
> * `dependencies` These are all of the dependencies for your project. This specific subcommand example requires `conda`, which is why it is listed here.
>
> For more information on `pyproject.toml` see the [PyPA packaging documentation][pyproject.toml docs].

</details>


Additionally, a `setup.py` file is required for the `cffi_modules` parameter:

```python
from setuptools import setup

setup(cffi_modules=["temp_converter/builder.py:ffibuilder"])
```

> **Note**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/editable install

The custom `temp-converter` subcommand plugin can be installed as an editable install by running the following command:


```bash
$ pip install -e .
```

To learn more about editable installs, please read the [corresponding pip documentation page][editable install doc].

### Packaging the custom subcommand using `conda-build`

When you're ready to distribute your custom `temp-converter` subcommand plugin, you can package it as a conda package:

<details>
<summary><code>recipe/meta.yaml</code></summary>

```yaml
package:
  name: temp-converter
  version: 1.0

source:
  path: ../

build:
  script: $PYTHON -m pip install --no-deps .

requirements:
  host:
    - python >=3.7
    - cffi>=1.0.0

  run:
    - conda
    - python >=3.7
    - cffi>=1.0.0

about:
  home: https://github.com/conda/conda-plugin-template
  license: BSD-3-Clause
  summary: A custom subcommand written in C that converts Celsius to Fahrenheit
```

</details>

```bash
$ conda build ./recipe
```

There is more detailed information available via the [`conda-build` documentation][build conda packages] on how to build conda packages from scratch. Please also check out [this documentation page][upload to anaconda.org] if you'd like to learn how to upload your subcommand package to [anaconda.org][anaconda.org site].

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
temp-converter - A custom subcommand written in C that converts Celsius to Fahrenheit

conda commands available from other packages (legacy):
content-trust
env
```

Running `conda temp-converter` will result in the following output:

```bash
$ conda temp-converter

Enter the temperature in Celsius:
4

4.00 Celsius = 39.20 Fahrenheit

```

Congratulations! 🎉 You've successfully implemented a conda subcommand plugin written in C! For further reference on how the plugin system works, check out the [official `pluggy` docs][pluggy docs].


> **Note**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

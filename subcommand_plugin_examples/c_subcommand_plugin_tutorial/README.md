[template]: https://github.com/conda/conda-plugin-template/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[editable install doc]: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[build conda packages]: https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html
[upload to anaconda.org]: https://docs.anaconda.com/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages
[anaconda.org site]: https://anaconda.org/
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugin-api/index.html#a-note-on-licensing
[pep 621]: https://peps.python.org/pep-0621/
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html

# Custom conda Subcommand Plugin Tutorial Written in C

In this tutorial, we will create a new conda subcommand written in C that converts Celsius to Fahrenheit.

To follow along with this guide, make sure you have the latest conda and conda-build installed:

```bash
$ conda update conda conda-build pip
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repository using this [template][template]):

```
c_subcommand_plugin/
├── recipe/
│   └── meta.yaml
├── LICENSE
├── c_subcommand.c
├── pyproject.toml (or setup.py)
└── conda_c_subcommand.py
```

## Implementing the C side of the subcommand plugin

First, create a C file (with a `.c` extension) that includes the required function(s):

```c
/**
* c_to_f.c
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

Next, create a shared library file (`.so` extension) using the C compiler by running the following command (from the same level as where `c_to_f.c` is located):

```
$ cc -fPIC -shared -o c_subcommand.so c_subcommand.c
```

After running that command, a new shared library file will be generated:

```
c_subcommand_plugin/
├── recipe/
│   └── meta.yaml
├── LICENSE
├── c_subcommand.c
├── c_subcommand.so
├── pyproject.toml (or setup.py)
└── conda_c_subcommand.py
```

## The custom subcommand module (the Python side of the subcommand plugin)

In the Python program (shown in the example below), a `ctypes.CDLL` instance will be created from the shared `.so` file that was generated in the previous step.

The `temp_conv_c.py` module can then call the C function using the format `CDLL(so_file)` from inside of the `conda_temp_converter()` function. Once that code is in place, then the `conda_temp_converter()` function can be registered via the plugin manager hook called `conda_subcommands` using the `@conda.plugins.register` decorator:

```python
# temp_conv_c.py

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
```

## Packaging the custom subcommand using `pyproject.toml`

In order to install the `conda temp-converter` custom subcommand, we will need to configure a Python build system. You can either use the [PEP 621][pep 621] compliant `pyproject.toml` or alternatively `setup.py` can be used (not shown in this tutorial):

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "temp-converter"
version = "1.0"
description = "A custom subcommand written in C that converts Celsius to Fahrenheit"
requires-python = ">=3.7"
dependencies = ["conda"]

[tools.setuptools]
py_modules=["temp-converter"]

[project.entry-points.conda]
temp-converter = "temp_conv_c"
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


> **Note:**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/editable install

The custom `temp-converter` subcommand plugin can be installed as an editable install by running the following command:


```bash
pip install -e .
```

To learn more about editable installs, please read the [corresponding pip documentation page][editable install doc].

### Packaging the custom subcommand using `conda-build`

When you're ready to distribute your custom `temp-converter` subcommand plugin you can package it as a conda package:

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

  run:
    - conda
    - python >=3.7

about:
  home: https://github.com/conda/conda-plugin-template
  license: BSD-3-Clause
  license_file: LICENSE
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


> **Note:**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

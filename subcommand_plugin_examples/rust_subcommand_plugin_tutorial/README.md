[template]: https://github.com/conda/conda-plugin-template/subcommand_plugin_examples/rust_subcommand_plugin_tutorial/generate
[pyproject.toml docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml
[entrypoints docs]: https://packaging.python.org/en/latest/specifications/entry-points/
[licenses]: https://docs.conda.io/projects/conda/en/latest/dev-guide/plugin-api/index.html#a-note-on-licensing
[pep 621]: https://peps.python.org/pep-0621/
[maturin]: https://github.com/PyO3/maturin
[pyo3]: https://github.com/PyO3/pyo3
[pluggy docs]: https://pluggy.readthedocs.io/en/stable/index.html

# Custom conda Subcommand Plugin Tutorial Written in Rust

In this tutorial, we will create a new conda subcommand written in Rust that multiplies two integers.

To follow along with this guide, make sure you have the latest conda and conda-build installed:

```bash
(base) $ conda update conda conda-build
```

## Project directory structure

Set up your working directory and files as shown below (or create a new repo using this [template][template]):

```
rust_subcommand_plugin/
├── Cargo.toml
├── recipe/
│   └── meta.yaml
├── LICENSE
├── pyproject.toml (or setup.py)
├── rust_plugin.py
└── src/
    └── lib.rs
```

## Implementing the Rust side of the subcommand plugin

Annotations (e.g., `#[pyfunction]` and `#[pymodule]`) available via [`pyo3`][pyo3] are utilized in the Rust program in order to enable it to be importable by the Python module:

```rust
// src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
// The original function is below
fn multiply(a: isize, b: isize) -> isize {
    a * b
}

#[pymodule]
fn rustiply(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    Ok(())
}
```

Once the Rust program is set up as shown in the example above, the Python module (`rust_plugin.py`, shown in the next section) that registers the subcommand via the plugin hook can import the Rust program successfully.

## The custom subcommand module (the Python side of the subcommand plugin)

The `rust_plugin.py` module in this example imports the `rustiply` function from `src.lib.rs` and calls it inside of the function `conda_rustiply()` (where two numbers multiplied) and then registers `conda_rustiply()` via the plugin manager hook called `conda_subcommands` using the `@conda.plugins.register` decorator:

```python
# rust_plugin.py

import rustiply
import argparse
import conda.plugins


def conda_rustiply(argv: list):
    parser = argparse.ArgumentParser("conda multiply")
    parser.add_argument("x", type=int, help="First number to multiply")
    parser.add_argument("y", type=int, help="Second number to multiply")

    args = parser.parse_args(argv)
    
    x = args.x
    y = args.y
    result = rustiply.multiply(x, y)
    print(f"\nThe product of {x} * {y} is: {result}\n")


@conda.plugins.register
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="multiply",
        summary="A subcommand written in Rust that multiplies two integers",
        action=conda_rustiply,
    )
```

## Packaging the custom subcommand

In order to install the `conda multiply` subcommand we will need to configure a Python build system. You can either use the [PEP 621][pep 621] compliant `pyproject.toml` or alternatively `setup.py` can be used (not shown in this tutorial).

Since [Maturin][maturin] is a dependency, it will need to be listed in the `pyproject.toml` file under the `[project]` section:

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "multiply"
version = "1.0"
description = "A subcommand that multiplies two integers"
requires-python = ">=3.7"
dependencies = ["conda", "maturin"]

[tools.setuptools]
py_modules=["multiply"]

[project.entry-points.conda]
multiply = "rust_plugin"
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
> * `dependencies` These are all of the dependencies for your project. This specific subcommand example requires both `conda` and `maturin`, which is why they are both listed here.
>
> For more information on `pyproject.toml` see the [PyPA packaging documentation][pyproject.toml docs].

</details>


> **Note:**
> For more information about entry points specification in general, please read [PyPA's entrypoints documentation][entrypoints docs].

### Development/Editable Install

The custom `multiply` subcommand plugin can be installed as an editable install by running the following from the directory where `pyproject.toml` is located:

```bash
$ pip install -e .
```

...and then make sure to run:

```
$ maturin develop
```

### Conda Install

When you're ready to distribute your custom `multiply` subcommand plugin, you can package it as a conda package:

<details>
<summary><code>recipe/meta.yaml</code></summary>

```yaml
package:
  name: multiply
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
    - maturin

about:
  home: https://github.com/conda/conda-plugin-template/subcommand_plugin_examples/rust_subcommand_plugin_tutorial/multiply
  license: BSD-3-Clause
  license_file: LICENSE
  summary: A subcommand written in Rust that multiplies two integers
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
multiply - A subcommand written in Rust that multiplies two integers

conda commands available from other packages (legacy):
content-trust
env
```

Running `conda multiply [two integers]` will result in the following output:

```bash
$ conda multiply 5 4

The product of 5 * 4 is: 20
```

Congratulations, you've successfully implemented a conda subcommand plugin written in Rust! For further reference on how the plugin system works, check out the [official `pluggy` docs][pluggy docs].

> **Note:**
> Whenever you develop your own custom plugins, please be sure to [apply the appropriate license][licenses].

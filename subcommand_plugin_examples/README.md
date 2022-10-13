# `conda` Subcommand Plugin Examples

## C Plugins 
<!-- Add link -->

From the top-level directory (_i.e._, `conda-plugin-template/subcommand_plugin_examples/c_subcommand_plugin_tutorial/temp_converter/`), run:

```
$ cc -fPIC -shared -o [program_name].so [program_name].c
```

... in order to create a shared library file (with the `.so` extension) using the C compiler. For example, in the `temp_converter` example, you would run:

```
$ cc -fPIC -shared -o c_to_f.so c_to_f.c
```

In the Python portion of the plugin (_i.e._, `conda-plugin-template/subcommand_plugin_examples/c_subcommand_plugin_tutorial/temp_converter/temp_conv_c.py`), we've created a `ctypes.CDLL` instance from the shared file and can thus call the C function using the format 
`{CDLL_instance}.{function_name}({function_parameters})`.


## Python Plugins
<!-- Add link -->
From the top-level directory (_i.e._, `conda-plugin-template/subcommand_plugin_examples/conda_subcommand_plugin_tutorial/`) run the following to execute an editable install via `pip`:

```
$ pip install -e .
```

## Rust Plugins
<!-- Add link -->
> **Note:** Make sure you have `maturin` installed.

From the top-level directory (_i.e._, `conda-plugin-template/subcommand_plugin_examples/rust_subcommand_plugin_tutorial/multiply/`) run the following to execute an editable install via `pip`:

```
$ pip install -e .
```

... and then run:

```
$ maturin develop
```
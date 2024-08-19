TODO: Please consider submitting a PR to the [conda-incubator/plugins] repo with a link to your new plugin!

# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Development

To begin developing for this project, source the `develop.sh` script (macOS and Linux only).
Run the following command from the root of your project directory.

```bash
source develop.sh
```

This will create a new environment in the `./env` folder of your project and modifies
`CONDA_EXE` to point to an isolated version of conda within this environment.

To update this environment when new dependencies are added to `environment.yml`, you
can run the same `source develop.sh` command as above.

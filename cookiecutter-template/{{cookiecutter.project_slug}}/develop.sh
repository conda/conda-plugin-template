# Used to switch CONDA_EXE to the one located in development environment
# To use this script, run `source develop.sh`

if ! (return 0 2> /dev/null); then
    echo "ERROR: Source this script: source '$0'." >&2
    exit 1
fi

CONDA_ENV_DIR="./env"

conda env $(test -d "$CONDA_ENV_DIR" && echo update || echo create) -p "$CONDA_ENV_DIR" --file environment.yml
conda activate "$CONDA_ENV_DIR"
pip install --no-deps --no-index --no-build-isolation -e .

CONDA_EXE="$CONDA_PREFIX/condabin/conda"

# setup.py (with automatic dependency tracking)
from setuptools import setup

setup(
    packages=["temp_converter"],
    cffi_modules=["temp_converter/builder.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
)

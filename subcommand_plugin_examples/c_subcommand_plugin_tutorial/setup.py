# setup.py (with automatic dependency tracking)
from setuptools import setup

setup(cffi_modules=["temp_converter/builder.py:ffibuilder"])

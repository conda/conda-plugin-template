# setup.py (required for cffi_modules parameter)
from setuptools import setup

setup(cffi_modules=["temp_converter/builder.py:ffibuilder"])

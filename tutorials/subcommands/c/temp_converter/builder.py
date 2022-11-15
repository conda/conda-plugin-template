# in a separate file "[package]/foo_build.py"
import pathlib

import cffi

c_to_f = pathlib.Path(__file__).parent / "c_to_f.c"

ffibuilder = cffi.FFI()
ffibuilder.set_source("temp_converter._converter", c_to_f.read_text())
ffibuilder.cdef("int converter();")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

import marshal
import struct
import time


def code_from_pyc(file):
    f = open(file, "rb")
    magic = f.read(12)
    code = marshal.load(f)
    return code

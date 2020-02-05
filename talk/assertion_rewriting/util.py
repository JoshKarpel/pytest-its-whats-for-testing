import time
import struct
import marshal

def code_from_pyc(file):
    f = open(file, "rb")
    magic = f.read(12)
    code = marshal.load(f)
    return code

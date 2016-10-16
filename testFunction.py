import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer

lib = ctypes.cdll.LoadLibrary("./ctest.so")

matmul_c = lib.matmul
matmul_c.restype = None
doublepp = ndpointer(ctypes.c_double, ndim=2, flags="C_CONTIGUOUS")
intcpp = ndpointer(ctypes.c_int8, ndim=2, flags="C_CONTIGUOUS")  # ndpointer(dtype=np.uintp, ndim=1, flags='C')

matmul_c.argtypes = [intcpp, doublepp, ctypes.c_int, ctypes.c_int, ctypes.c_int, doublepp]

np.random.seed(24)
nb_col = 5
nb_lig = 4
nb_out = 3

mat_binary = np.random.randint(2, size=(nb_lig, nb_col), dtype='int8')
mat_float = np.random.uniform(-1, 1, size=(nb_out, nb_col))

print(mat_binary)
print ''
print(mat_float)
print ''

res = np.ones((nb_out, nb_lig), dtype='double')

matmul_c(mat_binary, mat_float, nb_lig, nb_out, nb_col, res)
print(mat_binary)
print ''
print(mat_float)
print ''
print(res)
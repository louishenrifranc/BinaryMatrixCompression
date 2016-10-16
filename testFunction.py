import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import time
lib = ctypes.cdll.LoadLibrary("./ctest.so")

matmul_c = lib.matmul
matmul_c.restype = None
doublepp = ndpointer(ctypes.c_double, ndim=2, flags="C_CONTIGUOUS")
intcpp = ndpointer(ctypes.c_int8, ndim=2, flags="C_CONTIGUOUS")

matmul_c.argtypes = [intcpp, doublepp, ctypes.c_int, ctypes.c_int, ctypes.c_int, doublepp]

np.random.seed(24)
nb_hidden = 5
nb_in = 4
nb_out = 3

mat_binary = np.random.randint(2, size=(nb_in, nb_hidden), dtype='int8')
mat_float = np.random.uniform(-1, 1, size=(nb_out, nb_hidden))
res = np.ones((nb_in, nb_out), dtype='double')

# print(np.dot(mat_float, mat_binary.T))
start_time = time.time()
matmul_c(mat_binary, mat_float, nb_in, nb_out, nb_hidden, res)
print("C code--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
R = np.dot(mat_float, mat_binary.T)
print("Numpy --- %s seconds ---" % (time.time() - start_time))

print(res)
print(R)


# Perte d'informations il me semble (passage d'un double pas complet)
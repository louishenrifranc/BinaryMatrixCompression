import theano.tensor as T
import theano
import numpy as np
import time

np.show_config()
np.random.seed(42)
nb_col = 1000000
nb_lig = 100
nb_out = 100


mat_binary = np.random.randint(2, size=(nb_lig, nb_col))
mat_float = np.random.uniform(-1, 1, size=(nb_col, nb_out))


start_time = time.time()
A = theano.shared(np.asarray(mat_binary, dtype='int8'))
B = theano.shared(np.asarray(mat_float, dtype='float16'))
C = theano.dot(A, B)
f = theano.function([], C)
f()
# D = C.eval()
print("--- %s seconds ---" % (time.time() - start_time))



# Experiment 1 (using int8)
# A = theano.shared(np.asarray(mat_binary, dtype='int8'))
# B = theano.shared(np.asarray(mat_float, dtype='float32'))
# C = theano.dot(T.cast(A, 'float32'), B)
# --- 1.81055212021 seconds ---

# Experiment 2 (using float32 for both)
# A = theano.shared(np.asarray(mat_binary, dtype='float32'))
# B = theano.shared(np.asarray(mat_float, dtype='float32'))
# C = theano.dot(T.cast(A, 'float32'), B)
# "--- 1.94088482857 seconds ---


# Experiment 3 (using float16)
# A = theano.shared(np.asarray(mat_binary, dtype='int8'))
# B = theano.shared(np.asarray(mat_float, dtype='float16'))
# C = theano.dot(T.cast(A, 'float32'), B)
# Disabling C code for dot due to unsupported float16

# Experiment 4 (inverse order of operation float * int)
# A = theano.shared(np.asarray(mat_binary, dtype='float32'))
# B = theano.shared(np.asarray(mat_float, dtype='int8'))
# C = theano.dot(A, B)
# worse

# TUPLE are not modifiable
move = (10, 20, 30)

# LIST are modifiable
l = ['hllo', 10]
l.append(30)
l[1] = 0

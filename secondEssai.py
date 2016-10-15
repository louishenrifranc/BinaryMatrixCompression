import numpy as np
import time

nb_col = 1000000
nb_lig = 100
nb_out = 50
np.random.seed(42)


def mat_mul(x_, w_):
    """
    :param x_: the binary matrix of dim [n_sample,n_features]
    :param w_: the float matrix of dim [n_hidden, n_features]
    :return: w_.T dot x_
    """

    if len(x_.shape) > 2 | len(w_.shape) > 2:
        raise "Dimensions of matrix is too high"
    if x_.shape[1] != w_.shape[1]:
        raise "Dimensions are incorrect for matrix multiplication"

    z = np.zeros((x_.shape[0], w_.shape[0]))
    start_time = time.time()
    x_ = x_.T
    print("Transpose time %s seconds ---" % (time.time() - start_time))

    """ iterate over n_sample"""
    for i in range(x_.shape[1]):
        start_time = time.time()
        mask = np.where(x_[:, i] == 1)
        """ iterate over n_hidden """
        for j in range(w_.shape[0]):
            z[i, j] = w_[j][mask].sum()

    if i == 0:
        print("One iteration :%s seconds ---" % (time.time() - start_time))

    return z.T


mat_binary = np.random.randint(2, size=(nb_lig, nb_col))
mat_float = np.random.uniform(-1, 1, size=(nb_out, nb_col))

start_time = time.time()
R1 = mat_mul(mat_binary, mat_float)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
R2 = np.dot(mat_float, mat_binary.T)
print("--- %s seconds ---" % (time.time() - start_time))

assert(np.any(R1 != R2))



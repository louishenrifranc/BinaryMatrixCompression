import scipy.linalg.blas
import numpy as np
import time
import multiprocessing
import threading
from multiprocessing import Process

nb_col = 300000
nb_lig = 40
nb_out = 30


# np.random.seed(42)


def mat_mul_reverse(x_, w_):
    """
    :param x_: the binary matrix of dim [n_sample,n_features]
    :param w_: the float matrix of dim [n_hidden, n_features]
    :return: w_ dot x_.T
    """

    if len(x_.shape) > 2 | len(w_.shape) > 2:
        raise "Dimensions of matrix is too high"
    if x_.shape[1] != w_.shape[1]:
        raise "Dimensions are incorrect for matrix multiplication"

    z = np.empty((x_.shape[0], w_.shape[0]))
    """ iterate over n_sample"""
    for i in range(x_.shape[0]):
        mask = np.argwhere(x_[i, :] == 1)
        # z[i] = np.sum(w_[:, np.flatnonzero(x_[i, :] == 1)], axis=1)

        """ iterate over n_hidden """
        for j in range(w_.shape[0]):
            z[i, j] = w_[j][mask].sum()
    return z.T


class MatMul:
    def __init__(self, x_, w_):
        nb_cores = int(multiprocessing.cpu_count())

        if x_.shape[0] < nb_cores:
            self.z1_ = mat_mul_reverse(x_, w_)
        else:
            nb_op = x_.shape[0] / nb_cores
            self.z1_ = np.empty((x_.shape[0], w_.shape[0]))
            processes = []
            for i in range(nb_cores):
                min_i = i * nb_op
                max_i = (i + 1) * nb_op
                if i == nb_cores - 1:
                    max_i = x_.shape[0]
                p = Process(target=self.mat_mul_reverse_p, args=(x_, w_, min_i, max_i))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

        self.z1_ = self.z1_.T

    def mat_mul_reverse_p(self, x_, w_, min_index, max_index):
        """ iterate over n_sample"""
        for i in range(min_index, max_index):
            mask = np.where(x_[i, :] == 1)
            """ iterate over n_hidden """
            # self.z1_[i] = np.sum(w_[:, mask], axis=1)
            for j in range(w_.shape[0]):
                self.z1_[i, j] = np.sum(w_[j][mask])


def mat_mul_copy(x_, w_):
    """
    :param x_: the binary matrix of dim [n_sample,n_features]
    :param w_: the float matrix of dim [n_hidden, n_features]
    :return: w_.T dot x_
    """

    if len(x_.shape) > 2 | len(w_.shape) > 2:
        raise "Dimensions of matrix is too high"
    if x_.shape[1] != w_.shape[1]:
        raise "Dimensions are incorrect for matrix multiplication"

    z = np.zeros((w_.shape[0], x_.shape[0]))
    for i in range(w_.shape[0]):
        copy = w_[i]
        for j in range(x_.shape[0]):
            z[i, j] = np.sum(copy[np.where(x_[j] == 1)])
    return z


if __name__ == '__main__':
    mat_binary = np.random.randint(2, size=(nb_lig, nb_col))
    mat_float = np.random.uniform(-1, 1, size=(nb_out, nb_col))

    start_time = time.time()
    np.dot(mat_float, mat_binary.T)
    print("Reference numpy time : --- %s seconds ---" % (time.time() - start_time))

    """ not good time at all """
    # start_time = time.time()
    # R3 = mat_mul_copy(mat_binary, mat_float)
    # print("Mat Mul 1 copy--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    mat_mul_reverse(mat_binary, mat_float)
    print("Mat Mul reverse--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    m = MatMul(mat_binary, mat_float)
    print("Mat mul reverse parallel--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    scipy.linalg.blas.dgemm(alpha=1.0, a=mat_float.T, b=mat_binary.T, trans_a=True)
    print("Reference scipy time : --- %s seconds ---" % (time.time() - start_time))

# print(R1)
# print(R2)
# print(R3)
# print(m.z1_)

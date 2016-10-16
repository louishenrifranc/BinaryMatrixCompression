from secondEssai import mat_mul_reverse,np, MatMul, scipy, nb_lig, nb_out, time
import matplotlib.pyplot as plt


def plot_time():
    timel = [[] for i in range(5)]

    for i in (10, 100,1000,10000,100000,200000,300000,400000,500000,750000,1000000):
        nb_col = i
        timel[4].append(i)
        mat_binary = np.random.randint(2, size=(nb_lig, nb_col))
        mat_float = np.random.uniform(-1, 1, size=(nb_out, nb_col))

        start_time = time.time()
        np.dot(mat_float, mat_binary.T)
        timel[0].append(time.time() - start_time)

        start_time = time.time()
        mat_mul_reverse(mat_binary, mat_float)
        timel[1].append(time.time() - start_time)

        start_time = time.time()
        m = MatMul(mat_binary, mat_float)
        timel[2].append(time.time() - start_time)

        start_time = time.time()
        scipy.linalg.blas.dgemm(alpha=1.0, a=mat_float.T, b=mat_binary.T, trans_a=True)
        timel[3].append(time.time() - start_time)
    # print(timel[0])

    plt.plot(timel[4], timel[0], 'r', label="numpy")
    plt.plot(timel[4], timel[1], 'b', label="mat_mul_reverse")
    plt.plot(timel[4], timel[2], 'g', label="mat_mul_reverse_parallel")
    plt.plot(timel[4], timel[3], 'p', label="scipy Fortran style")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plot_time()

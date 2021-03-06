import sys
import numpy as np
import matplotlib.pyplot as plt

precision = 16
eps = 10 ** (- precision)


def read_matrix(path):
    with open(path) as f:
        lines = f.readlines()

    n = int(lines[0])
    lines = lines[2:]

    mp = [{} for _ in range(n)]

    for line in lines:
        val, i, j = line.split(',')
        val = float(val.strip())
        i = int(i.strip())
        j = int(j.strip())

        if i == j and abs(val) < eps:
            sys.exit('Null element on main diagonal')

        if mp[i].get(j) is not None:
            mp[i][j] += val
            continue

        mp[i][j] = val

    return n, mp


# Another way of memorizing the rare matrix
def read_matrix_special(path):
    # using the first method of memorizing the matrix because of the duplicate elements
    n, a = read_matrix(path)

    for i in range(n):
        for j, value in a[i].items():
            a[j][i] = value

    num = []
    poz = []

    for i in range(n):
        for j, value in a[i].items():
            num.append(value)
            poz.append(n * i + j)

    return n, num, poz


def read_line_matrix(path, n):
    matrix = np.zeros((n, 1), dtype='float32')

    with open(path) as f:
        lines = f.readlines()

    for i in range(len(lines)):
        matrix[i, 0] = float(lines[i].strip())

    return matrix


# The dot product between a and b
def product(a, x):
    n = len(a)

    pr = np.zeros((n, 1), dtype='float32')

    for i in range(n):
        su = 0
        for j, value in a[i].items():
            su += x[j, 0] * value

        pr[i, 0] = su

    return pr


def product_special(num, poz, x):
    n = len(x)

    pr = np.zeros((n, 1), dtype='float32')

    ci = 0
    su = 0

    for k in range(len(num)):
        number = num[k]
        i = poz[k] // n
        j = poz[k] % n

        if ci != i:
            pr[ci, 0] = su
            ci = i
            su = 0

        su += number * x[j, 0]

    if su != 0:
        pr[n - 1, 0] = su

    return pr


# |Ax - b|
def check_with_real_solution(a, b, x):
    pr = product(a, x)
    return np.linalg.norm(pr - b)


# |Ax - b|
def check_with_real_solution_special(num, poz, b, x):
    pr = product_special(num, poz, x)
    return np.linalg.norm(pr - b)


def jacobi_method(a, b, eps):
    n = len(a)

    x_prev = np.zeros((n, 1), dtype='float32')
    x_current = np.zeros((n, 1), dtype='float32')

    for i in range(n):
        for j, value in a[i].items():
            a[j][i] = value

    dx_progress = []
    solution_progress = []

    for iteration in range(10000):
        for i in range(n):
            su = 0
            for j, value in a[i].items():
                if j == i:
                    continue

                su += x_prev[j, 0] * value

            x_current[i, 0] = (b[i] - su) / a[i][i]

        DX = np.linalg.norm(x_current - x_prev)
        sol = check_with_real_solution(a, b, x_current)

        dx_progress.append(DX)
        solution_progress.append(sol)

        x_prev = x_current.copy()

        print(DX)
        print(sol)

        if DX < eps:
            plt.show()
            print(f'Solution found in {iteration} iterations')
            break

        if DX > (10 ** 8):
            plt.show()
            print(f'Divergence')
            break

    return x_current, dx_progress, solution_progress


def jacobi_method_special(num, poz, n, b, eps):
    x_prev = np.zeros((n, 1), dtype='float32')
    x_current = np.zeros((n, 1), dtype='float32')

    dx_progress = []
    solution_progress = []

    diag = []

    for k in range(len(num)):
        number = num[k]
        i = poz[k] // n
        j = poz[k] % n

        if i == j:
            diag.append(number)

    for iteration in range(10000):

        ci = 0
        su = 0

        for k in range(len(num)):
            number = num[k]
            i = poz[k] // n
            j = poz[k] % n

            if i == j:
                continue

            if ci != i:
                x_current[ci, 0] = (b[ci] - su) / diag[ci]
                ci = i
                su = 0

            su += number * x_prev[j, 0]

        if su != 0:
            x_current[n - 1, 0] = (b[n - 1] - su) / diag[n - 1]

        DX = np.linalg.norm(x_current - x_prev)
        sol = check_with_real_solution_special(num, poz, b, x_current)

        dx_progress.append(DX)
        solution_progress.append(sol)

        x_prev = x_current.copy()

        print(DX)
        print(sol)

        if DX < eps:
            plt.show()
            print(f'Solution found in {iteration} iterations')
            break

        if DX > (10 ** 8):
            plt.show()
            print(f'Divergence')
            break

    return x_current, dx_progress, solution_progress


def show_progress(dx_progress, sol_progress, title):
    line1, = plt.plot(dx_progress, label='DX')
    line2, = plt.plot(sol_progress, label='Sol Conv')
    plt.legend(handles=[line1, line2])
    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel('Progress')
    # You can do either show or save
    # plt.show()
    plt.savefig(f'plots/{title}.png')


def main():
    n_a1, a1 = read_matrix('a_1.txt')
    n_a2, a2 = read_matrix('a_2.txt')
    n_a3, a3 = read_matrix('a_3.txt')
    n_a4, a4 = read_matrix('a_4.txt')
    n_a5, a5 = read_matrix('a_5.txt')

    b1 = read_line_matrix('b_1.txt', n_a1)
    b2 = read_line_matrix('b_2.txt', n_a2)
    b3 = read_line_matrix('b_3.txt', n_a3)
    b4 = read_line_matrix('b_4.txt', n_a4)
    b5 = read_line_matrix('b_5.txt', n_a5)

    # Uncomment the one that you want to verify

    x, dx_progress, sol_progress = jacobi_method(a1, b1, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a1')
    print(x)

    x, dx_progress, sol_progress = jacobi_method(a2, b2, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a2')
    print(x)

    x, dx_progress, sol_progress = jacobi_method(a3, b3, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a3')
    print(x)

    x, dx_progress, sol_progress = jacobi_method(a4, b4, 0.126)
    show_progress(dx_progress, sol_progress, 'Progress for a4')
    print(x)

    x, dx_progress, sol_progress = jacobi_method(a5, b5, 1)
    show_progress(dx_progress, sol_progress, 'Progress for a5')
    print(x)

    # # Another way of memorizing the rare matrix
    n_a1, num1, poz1 = read_matrix_special('a_1.txt')
    x, dx_progress, sol_progress = jacobi_method_special(num1, poz1, n_a1, b1, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a1 special')
    print(x)

    n_a2, a2, poz2 = read_matrix_special('a_2.txt')
    x, dx_progress, sol_progress = jacobi_method_special(a2, poz2, n_a2, b2, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a2 special')
    print(x)

    n_a3, a3, poz3 = read_matrix_special('a_3.txt')
    x, dx_progress, sol_progress = jacobi_method_special(a3, poz3, n_a3, b3, 0.0001)
    show_progress(dx_progress, sol_progress, 'Progress for a3 special')
    print(x)

    n_a4, a4, poz4 = read_matrix_special('a_4.txt')
    x, dx_progress, sol_progress = jacobi_method_special(a4, poz4, n_a4, b4, 0.126)
    show_progress(dx_progress, sol_progress, 'Progress for a4 special')
    print(x)

    n_a5, a5, poz5 = read_matrix_special('a_5.txt')
    x, dx_progress, sol_progress = jacobi_method_special(a5, poz5, n_a5, b5, 0.1)
    show_progress(dx_progress, sol_progress, 'Progress for a5 special')
    print(x)


if __name__ == '__main__':
    main()

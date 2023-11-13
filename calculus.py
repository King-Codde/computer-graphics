import math


def get_bezier_basis(i, n, t):
    basis = (math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))*math.pow(t, i)*math.pow(1-t, n-i)
    return basis


def get_bezier(dots):
    step = 0.01
    result = []
    ind = t = 0
    while t <= 1:
        result.append([0, 0])
        for i in range(len(dots)):
            b = get_bezier_basis(i, len(dots) - 1, t)

            result[ind][0] += dots[i][0] * b
            result[ind][1] += dots[i][1] * b
        ind += 1
        t += step
    return result
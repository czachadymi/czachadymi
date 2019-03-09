import time
import math
import numpy

def makespan(sequence, sum_machines, machines):
    c_max = numpy.zeros((machines, len(sequence) + 1))
    for j in range(1, len(sequence) + 1):
        c_max[0][j] = c_max[0][j - 1] + sum_machines[0][sequence[j - 1]]

    for i in range(1, machines):
        for j in range(1, len(sequence) + 1):
            c_max[i][j] = max(c_max[i - 1][j], c_max[i][j - 1]) + sum_machines[i][sequence[j - 1]]
    return c_max

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p
            xs[low], xs[i] = xs[i], xs[low]

def main():
    dane = [0,1,2,3]
    parts = [[4,4,10,6], [5,1,4,10]]
    machines = len(parts)
    jobs = len(parts[0])
    for p in permute(dane):
        print("Cmax dla permutacji {} jest rowny {}".format(p,makespan(p, parts, machines)[machines - 1][jobs] ))



if __name__ == "__main__":
    main()

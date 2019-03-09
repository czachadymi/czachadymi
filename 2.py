import numpy


def dane():
    #parts = [[5,4,4,3],[5,5,4,5],[3,2,5,7]]
    #parts = [[6,10,4,7,6,5],[4,8,9,2,3,6]]
    parts = [[4,4,30,6,2],[5,1,4,30,3]] # http://www.rspq.org/pubs/j2.pdf # Cmax 47
    jobs = len(parts[0]) # if parts are the same length p1 = p2 = p3 = pn https://ieda.ust.hk/dfaculty/ajay/courses/ieem513/GT/johnson.html
    machines = len(parts) # amount of machines
    return machines, jobs, parts

def makespan(sequence, sum_machines, machines):
    c_max = numpy.zeros((machines, len(sequence) + 1))
    for j in range(1, len(sequence) + 1):
        c_max[0][j] = c_max[0][j - 1] + sum_machines[0][sequence[j - 1]]

    for i in range(1, machines):
        for j in range(1, len(sequence) + 1):
            c_max[i][j] = max(c_max[i - 1][j], c_max[i][j - 1]) + sum_machines[i][sequence[j - 1]]
    """
    print("***************")
    print(c_max)
    print('***************')
    """
    return c_max


def L1(data, jobs):
    l1 = []
    for j in range(jobs):
        if data[0][j] <= data[1][j]:
            l1.append(j)
    return sorted(l1, key=lambda l: data[0][l])


def L2(data, jobs):
    l2 = []
    for j in range(jobs):
        if data[0][j] > data[1][j]:
            l2.append(j)
    return sorted(l2, key=lambda l: data[1][l], reverse=True)


def johnson(data, machines, jobs):
    final_op = L1(data, jobs) + L2(data, jobs)
    return final_op, makespan(final_op, sum_machines, machines)[machines - 1][jobs]



machines, jobs, sum_machines = dane()
seq, cmax = johnson(sum_machines, machines, jobs)
print("Amount of Machines:", machines)
print("Amount of jobs:", jobs)
print("Machines operations in parts: ", sum_machines)
print("Johnson algorithm: {},  Cmax: {}".format(seq, cmax) )

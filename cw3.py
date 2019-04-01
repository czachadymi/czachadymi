import numpy


def dane(filename):
    with open(filename, "r") as data:
        machines = int(data.readline())
        jobs = int(data.readline())
        parts = numpy.zeros((machines, jobs))
        for i in range(machines):
            temp = data.readline().split()
            for j in range(jobs):
                parts[i][j] = int(temp[j])

    parts=numpy.transpose(parts)
    print('--------')
    print(parts)
    print('--------')
    temp = machines
    machines = jobs
    jobs = temp
    return machines, jobs, parts

def makespan(sequence, sum_machines, machines):
    c_max = numpy.zeros((machines, len(sequence) + 1))
    for j in range(1, len(sequence) + 1):
        c_max[0][j] = c_max[0][j - 1] + sum_machines[0][sequence[j - 1]]

    for i in range(1, machines):
        for j in range(1, len(sequence) + 1):
            c_max[i][j] = max(c_max[i - 1][j], c_max[i][j - 1]) + sum_machines[i][sequence[j - 1]]
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

def final_time(job, data, machines): # 2 posorowanie nierosnaco
    final = 0
    for i in range(machines):
        final += data[i][job]
    return final

# porzadkowanie kolejnosci
def prepNeh(data, machines, jobs):
    prepTemp = []
    for j in range(jobs):
        prepTemp.append(j)
    return sorted(prepTemp, key=lambda x: final_time(x, data, machines), reverse=True)

def sortNeh(seq, pos, value): # wstawianie zadania na pozycje "value"
    finalSeq = seq[:]
    finalSeq.insert(pos, value)
    return finalSeq

def neh(data, nb_machines, nb_jobs): #glowny neh
    order_seq = prepNeh(data, nb_machines, nb_jobs)
    seq_current = [order_seq[0]]
    for i in range(1, nb_jobs):
        min_cmax = float("inf")
        for j in range(0, i + 1):
            tmp_seq = sortNeh(seq_current, j, order_seq[i])
            cmax_tmp = makespan(tmp_seq, data, machines)[nb_machines - 1][len(tmp_seq)]
            print(tmp_seq, cmax_tmp)
            if min_cmax > cmax_tmp:
                best_seq = tmp_seq
                min_cmax = cmax_tmp
        seq_current = best_seq
    return seq_current, makespan(seq_current, data, machines)[machines - 1][jobs]



machines, jobs, sum_machines = dane("test.txt")
seq, cmax = neh(sum_machines, machines, jobs)
print("Amount of Machines:", machines)
print("Amount of jobs:", jobs)
print("Machines operations in parts: ", sum_machines)
print("Neh algorithm: {},  Cmax: {}".format(seq, cmax) )

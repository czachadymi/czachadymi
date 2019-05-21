from collections import OrderedDict as od
from copy import deepcopy
import re
import time


def PTM_Shrage(data):
    jobs = od(sorted(data.items(), key=lambda x: x[0]))
    job_copy = deepcopy(jobs)
    ready = od()
    t = 0
    cmax = 0
    l = None

    while ready or jobs:
        while jobs and min(jobs.values(), key=lambda x: x[0])[0] <= t:
            tmp = min(jobs.items(), key=lambda x: x[1][0])
            ready.update({tmp[0]: tmp[1]})
            del jobs[tmp[0]]
            if l is not None:
                if tmp[1][2] > job_copy[l][2]:
                    job_copy[l][1] = t - tmp[1][0]
                    t = tmp[1][0]
                    if job_copy[l][1] > 0:
                        ready.update({l: job_copy[l]})
        if not ready:
            t = min(jobs.values(), key=lambda x: x[0])[0]
        else:
            tmp = max(ready.items(), key=lambda x: x[1][2])
            del ready[tmp[0]]
            l = tmp[0]
            t += tmp[1][1]
            cmax = max(cmax, t + tmp[1][2])

    return cmax


def obtain_C(data, path):
    jobs = od((x, data[x]) for x in path)
    qb = jobs[path[-1]][2]
    for c in path[-2::-1]:
        if jobs[c][2] < qb:
            return c
    return None

def schrage(data):
    jobs = od(sorted(data.items(), key=lambda x: x[0]))
    ready = od()
    order = []
    cooled = []
    t = min(jobs.values(), key=lambda x: x[0])[0]

    while ready or jobs:
        avaible = od(i for i in jobs.items() if i[1][0] <= t)
        ready.update(avaible)
        for i in avaible.keys():
            del jobs[i]
        if not ready:
            t = min(jobs.values(), key=lambda x: x[0])[0]
        else:
            long = max(ready.items(), key=lambda x: x[1][2])
            del ready[long[0]]
            order.append(long[0])
            t += long[1][1]
            cooled.append((order[-1], t + long[1][2]))

    return order, max(cooled, key=lambda x: x[1])[1],\
        sorted(cooled, key=lambda x: x[1])[-1][0]



def variables(data, path):
    jobs = od((x, data[x]) for x in path)
    rk = min(jobs[x][0] for x in path)
    qk = min(jobs[x][2] for x in path)
    pk = sum(jobs[x][1] for x in path)

    return rk, qk, pk

def CRIT(data, order, b):
    jobs = od((x, data[x]) for x in order)
    crit = [order[0]]
    done = sum(jobs[order[0]][:-1])
    for i in order[1:order.index(b)+1]:
        if jobs[i][0] > done:
            crit.clear()
            crit.append(i)
            done = sum(jobs[i][:-1])
        else:
            crit.append(i)
            done += jobs[i][1]
    return crit


def CMAX(data, order):
    Full_time = sum(data[order[0]][:-1])
    Qk = [sum(data[order[0]][:-1]) + data[order[0]][2]]
    for i in order[1:]:
        if data[i][0] > Full_time:
            Full_time = sum(data[i][:-1])
            Qk.append(Full_time + data[i][2])
        else:
            Full_time += data[i][1]
            Qk.append(Full_time + data[i][2])
    return max(Qk)


def do_Carlier(data, UB):


    jobs = deepcopy(data)
    Ub = UB
    distribution, U, b = schrage(jobs) #1

    #pierwsza czesc

    if U < Ub: #2
        Ub = U
        done = distribution

    path = CRIT(jobs, distribution, b)
    real_C = obtain_C(jobs, path) #3
    temp = real_C

    if real_C is None:#4
        return done

    idxc = path.index(real_C)
    k = path[idxc+1:]
    Rk, Qk, Pk = variables(jobs, k) #5
    RPC = jobs[real_C][0]

    #druga część

    jobs[real_C][0] = max(RPC, Rk + Pk) #6
    lb = PTM_Shrage(jobs) #7
    lb = max(sum([Rk, Qk, Pk]), sum(variables(jobs, path[idxc:])), lb)
    if lb < Ub:#8
        return do_Carlier(jobs, UB)#9
    jobs[real_C][0] = RPC
    QPC = jobs[real_C][2] #10
    jobs[real_C][2] = max(QPC, Qk + Pk)#11
    lb = PTM_Shrage(jobs) #12
    lb = max(sum([Rk, Qk, Pk]), sum(variables(jobs, path[idxc:])), lb)
    if lb < Ub: #13
        return do_Carlier(jobs, UB)#14
    jobs[real_C][2] = QPC
    return done

def file_reader(name):
    with open(name, encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d+:')
        end = re.compile(r'\n')
        flag = False
        for line in lines:
            if re.match(start, line):
                data = []
                flag = True
                continue
            if re.fullmatch(end, line):
                flag = False
            if flag:
                tmp = list(map(int, line.split()))
                data.append(tmp)
                if data[0][0] + 1 == len(data):
                    yield {key: value for key, value in enumerate(data[1:])}
        return StopIteration

samples = file_reader("data2.txt")
for i, sample in enumerate(samples):
    print("Wyniki ze "+str(i+1)+" instancji")
    last = do_Carlier(sample, 1000000)
    print(CMAX(sample, last))
    print(last)

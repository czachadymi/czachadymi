from collections import OrderedDict as od
import re


def schrage(data):
    tasks = od(sorted(data.items(), key=lambda x: x[0]))
    tasks1 = tasks
    gotowy = od()
    kolej = []
    ostudzo = []
    t = min(tasks.values(), key=lambda x: x[0])[0]
    end = 0
    while gotowy or tasks:
        dostep = od(i for i in tasks.items() if i[1][0] <= t)
        gotowy.update(dostep)
        for i in dostep.keys():
            del tasks[i]
        if not gotowy:
            t = min(tasks.values(), key=lambda x: x[0])[0]
        else:
            long = max(gotowy.items(), key=lambda x: x[1][2])
            del gotowy[long[0]]
            kolej.append(long[0])
            t += long[1][1]
        ostudzo.append(t + long[1][2])
    return kolej, max(ostudzo)


def file_reader():
    with open("schr.data_n.txt", encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d:')
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


examples = file_reader()
for i, example in enumerate(examples):
    if i == i:
        kolejnosc, cmax = schrage(example)
        print("Kolejnosc:\n",kolejnosc)
        print("Cmax wynosi: ", cmax)

import random as r
import re
from math import exp
import time



"czytanie danych z pliku"
def read():
    with open("neh.data.txt") as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d{3}:')
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
                if data[0][0]+1 == len(data):
                    yield [[data[i][y] for i in range(1, len(data))] for y in range(data[0][1])]
        return StopIteration

"Ustawienie poprawnej wartości w tablicy"
def appendtab(pattern, *args):
    tab = []
    for arg in args:
        tab.append([arg[i-1] for i in pattern])
    return tab

"Generowanie rozwiązania początkowego"
def init(*args):
    border = [[] for i in range(len(args))]
    border[0] = [sum(args[0][:i]) for i in range(1, len(args[0]) + 1)]
    for n in range(len(args[0])):
        for i in range(1, len(args)):
            if n == 0:
                border[i].append(border[i - 1][n] + args[i][n])
            else:
                if border[i - 1][n] > border[i][n - 1]:
                    border[i].append(border[i - 1][n] + args[i][n])
                else:
                    border[i].append(border[i][n - 1] + args[i][n])
    return border[len(args) - 1][len(args[0]) - 1]


"Generowanie sąsiada"
def generate_n(answer):
    n_solve = answer[::]
    index = r.sample(list(range(len(answer))), 2)
    n_solve[index[0]], n_solve[index[1]] = n_solve[index[1]], n_solve[index[0]]
    return n_solve

"Prawdopodobieństwo przejścia"
def prob_trans(cmax, cmax_bis, t):
    if t == 0:
        return -1
    elif cmax_bis >= cmax:
        return exp((cmax-cmax_bis)/t)
    else:
        return 1

"Wykonaj ruch"
def move(*args):
    task = [args[i][0] for i in range(len(args))]
    task = [[task[z][y] for z in range(len(task))] for y in range(len(task[0]))]
    return task


"Schładzanie"
def chill(t, param=None, k=None, k_max=None):
    if param:
        return param * t
    return t*(k/k_max)

"Końcowa kolejność"
def solve(*args):
    tasks = list(zip(*args))
    task = [[v, i] for i, v in enumerate(tasks)]
    answer = task[::]
    r.shuffle(answer)
    t = 200
    iteration = 10000
    for i in range(iteration):
        b_answer = generate_n(answer)
        p = prob_trans(init(*move(*answer)), init(*move(*b_answer)), t)
        if p >= r.uniform(0, 1):
            answer = b_answer
        t = chill(t, param=0.99)
    answer = [answer[i][1] for i in range(len(answer))]
    return list(map(lambda x: x+1, answer))


if __name__ == '__main__':
    examples = read()
    for exa, end in enumerate(examples):
        if exa == 38:
            sek = solve(*end)
            print("Czas CMax poczatkowy", init(*end))
            print("Czas CMax końcowy", init(*appendtab(sek, *end)))
            print(sek)


#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import re
from itertools import combinations_with_replacement
from time import sleep
from getprob import *


class Clue(object):
    def __init__(self, clues):
        self.len = len(clues)
        self.clues = clues

    def __str__(self):
        ret = []
        for i in range(len(self.clues)):
            # ret.append(bcolors.OKGREEN if complete[i] else bcolors.FAIL
            ret.append(str(self.clues[i]))
        return ' '.join(ret)

    def get(self, i):
        return self.clues[i]

    def len_std_form(self):
        # ex) 1 2 3 --> ■X■■X■■■
        return sum(self.clues) + len(self.clues) - 1


class Problem(object):
    def __init__(self, title):
        self.size = [0, 0]
        self.RC = []
        self.CC = []
        self.ans = []
        self.print_string = None
        self.all_cases = {'r': {}, 'c': {}}
        self.title = title

    def add_clue(self, new, orient='r'):
        if orient not in ['r', 'c']:
            print("invalid orient type")
            return False

        if orient == 'r':
            self.RC.append(new)
            self.size[0] += 1
            self.ans.append([-1 for _ in range(self.size[1])])
        else:
            self.CC.append(new)
            self.size[1] += 1
            for i in range(self.size[0]):
                self.ans[i].append(-1)

        return True

    # def print_problem(self, orient=None, idx=-1, char=['□', '■', ' ']):
    def print_problem(self, orient=None, idx=-1, char=['X', '■', ' ']):
        if orient is not None and orient not in ['r', 'c']:
            print("invalid orient type")
            return False

        RCstr = list(map(str, self.RC))
        max_P = max(map(len, RCstr))
        CCstr = list(map(str, self.CC))
        max_Q = max(map(len, CCstr))
        # max_Q = max(map(len, Q))

        if self.print_string == None:
            self.print_string = self.title + '\n'
            for i in range(max_Q):
                tmp = ' ' * max_P + '|'
                tmp += '|'.join(map((lambda q: q[i - (max_Q - len(q))] if i >= (max_Q - len(q)) else ' '), CCstr))
                self.print_string += (tmp + '\n')

            self.print_string += '-' * max_P + '+' + '-' * (2 * len(self.CC)) + '\n'

        string = self.print_string
        for i in range(self.size[0]):
            # p = ' '.join(map(str, P[i]))
            # string += ' ' * (max_P - len(p)) + p

            string += ('{0:>{max_P}}'.format(''.join(map(str, RCstr[i])), max_P=max_P)) + '|'
            # string += ' '.join(map(lambda a: ' ' if a < 0 else '■' if a else '□', self.ans[i]))
            string += ' '.join(map(lambda a: char[a], self.ans[i]))
            if orient == 'r' and i == idx:
                string += ' <\n'
            else:
                string += '\n'

        if orient == 'c':
            string += ('{0:>{max_P}}'.format(' ', max_P=max_P)) + ' '
            string += ' ' * (2 * idx) + '^\n'

        print(string)
        return string

    def get_all_case(self, i, orient='r'):
        if orient not in ['r', 'c']:
            print("invalid orient type")
            return False

        axis = 1 if orient == 'r' else 0
        clues = self.RC[i] if orient == 'r' else self.CC[i]
        n = clues.len
        margin = self.size[axis] - clues.len_std_form()
        all_cases = []
        for comb in combinations_with_replacement(range(n + 1), margin):
            case = [1 for _ in range(n + 1)]
            case[0] = 0
            case[-1] = 0
            for i in comb:
                case[i] += 1

            case_list = [0 for _ in range(case[0])]
            for i in range(n):
                case_list += [1 for _ in range(clues.get(i))]
                case_list += [0 for _ in range(case[i + 1])]

            all_cases.append(case_list)

        return all_cases

    def find_with_hint(self, all_cases, idx, orient='r'):
        if orient not in ['r', 'c']:
            print("invalid orient type")
            return False

        if orient == 'r':
            hint = self.ans[idx]
        else:
            hint = [self.ans[i][idx] for i in range(self.size[0])]

        axis = 1 if orient == 'r' else 0
        candidate = set()
        for i, case in enumerate(all_cases):
            if all(hint[j] == -1 or case[j] == hint[j] for j in range(self.size[axis])):
                candidate.add(i)

        candidate = [case for i, case in enumerate(all_cases) if i in candidate]

        N = self.size[axis]
        for i in range(N):
            try:
                if all(case[i] == candidate[0][i] for case in candidate):
                    if orient == 'r':
                        self.ans[idx][i] = candidate[0][i]
                    else:
                        self.ans[i][idx] = candidate[0][i]
            except:
                print(N, i, orient, idx, len(hint))
                print(len(candidate))
                print(len(candidate[0]))
                exit(0)

    def row_step(self, idx):
        old_ans = self.ans[idx][:]
        if idx not in self.all_cases['r'].keys():
            self.all_cases['r'][idx] = self.get_all_case(idx, orient='r')
        all_cases = self.all_cases['r'][idx]
        self.find_with_hint(all_cases, idx, orient='r')

        return old_ans == self.ans[idx]

    def col_step(self, idx):
        old_ans = [self.ans[i][idx] for i in range(self.size[0])]
        if idx not in self.all_cases['c'].keys():
            self.all_cases['c'][idx] = self.get_all_case(idx, orient='c')
        all_cases = self.all_cases['c'][idx]
        self.find_with_hint(all_cases, idx, orient='c')

        new_ans = [self.ans[i][idx] for i in range(self.size[0])]
        return old_ans == new_ans

    def solve(self, v=False, t=0):
        self.obvious_proc()
        # self.print_problem()
        Ridx = list(range(self.size[0]))
        Cidx = list(range(self.size[1]))
        while True:
            done = []
            flag = True
            for idx in Ridx:
                ret = self.row_step(idx)
                flag = ret and flag

                if all(x >= 0 for x in self.ans[idx]):
                    done.append(idx)

                if v:
                    os.system('clear')
                    self.print_problem(orient='r', idx=idx)
                    sleep(t)
            Ridx = [i for i in Ridx if i not in done]
            # self.print_problem()
            if flag:
                break

            done = []
            flag = True
            for idx in Cidx:
                ret = self.col_step(idx)
                flag = ret and flag

                if all(self.ans[i][idx] >= 0 for i in range(self.size[0])):
                    done.append(idx)

                if v:
                    os.system('clear')
                    self.print_problem(orient='c', idx=idx)
                    sleep(t)
            Cidx = [i for i in Cidx if i not in done]
            # self.print_problem()
            if flag:
                break

        for i in range(len(self.ans)):
            for j in self.ans[i]:
                if j == -1:
                    return False

        return True

    def obvious_proc(self):
        # row process
        for i in range(self.size[0]):
            LeftTail = 0
            TotalMin = self.RC[i].len_std_form()
            for j in range(self.RC[i].len):
                LeftMinIdx = LeftTail + self.RC[i].get(j)
                RightMaxIdx = self.size[1] - TotalMin + LeftTail

                if RightMaxIdx < LeftMinIdx:
                    for idx in range(RightMaxIdx, LeftMinIdx):
                        self.ans[i][idx] = 1

                LeftTail += self.RC[i].get(j) + 1

        # col process
        for i in range(self.size[1]):
            LeftTail = 0
            TotalMin = self.CC[i].len_std_form()
            for j in range(self.CC[i].len):
                LeftMinIdx = LeftTail + self.CC[i].get(j)
                RightMaxIdx = self.size[0] - TotalMin + LeftTail

                if RightMaxIdx < LeftMinIdx:
                    for idx in range(RightMaxIdx, LeftMinIdx):
                        self.ans[idx][i] = 1

                LeftTail += self.CC[i].get(j) + 1


visual = False
interval = 0
for i, arg in enumerate(sys.argv):
    if arg[0] == '-':
        if arg[1] == 'v':
            visual = True
        elif arg[1] == 't':
            visual = True
            try:
                interval = float(sys.argv[i + 1])
            except:
                print("wrong command-line argument")

# file_list = [fn for fn in os.listdir('./') if re.match("problem[0-9*].txt", fn)]
# for i in range((len(file_list)-1)//4 + 1):
#     print (' '.join(file_list[4*i:4*(i+1)]))

# pnum = int(raw_input("Problem number: "))
# filename = 'problem' + str(pnum) + '.txt'
# with open(filename, "r") as f:
#     M, N = map(int, f.readline().split())
#     for i in range(M):
#         new = Clue(tuple(map(int, f.readline().split())))
#         Prob.add_clue(new, orient='r')

#     for i in range(N):
#         new = Clue(tuple(map(int, f.readline().split())))
#         Prob.add_clue(new, orient='c')

# popular = -5 notSolved = -2 local = 0
pagenum = 0
while True:
    os.system('clear')
    print("Visual: " + ("True" if visual else "False") + ("\tInterval: " + str(interval) if visual else ''))
    print("0: Local Problem\t1: Popular Problem")
    print("5, 10, 15, 20, 25: nxn Random Problem")
    print("q: Quit\n")

    sel = int(raw_input())

    os.system('clear')

    if sel == 0:
        os.system('clear')
        file_list = [fn for fn in os.listdir('./') if re.match("problem[0-9*].txt", fn)]
        for i in range((len(file_list) - 1) // 4 + 1):
            print(' '.join(file_list[4 * i:4 * (i + 1)]))

        pnum = int(raw_input("Problem number: "))
        filename = 'problem' + str(pnum) + '.txt'
        Prob = Problem(filename)
        with open(filename, "r") as f:
            M, N = map(int, f.readline().split())
            for i in range(M):
                new = Clue(tuple(map(int, f.readline().split())))
                Prob.add_clue(new, orient='r')

            for i in range(N):
                new = Clue(tuple(map(int, f.readline().split())))
                Prob.add_clue(new, orient='c')

    # popular = -5 notSolved = -2 local = 0
    elif sel != 'q':
        while True:
            os.system('clear')
            if sel == 1:
                prob_list = get_prob_list(pagenum, -5)
                title_list = list(prob_list.keys())
                for i, title in enumerate(title_list):
                    print("(%d) %s" % (i + 1, title))

            elif sel % 5 == 0 and sel in range(5, 30):
                prob_list = get_prob_list(pagenum, sel)
                title_list = list(prob_list.keys())
                for i, title in enumerate(title_list):
                    print("(%d) %s" % (i + 1, title))

            else:
                print("wrong input")
                exit(-1)

            pnum = raw_input("Input Problem Number or 'n' for next page... ")
            if pnum == 'n':
                pagenum += 1
                continue
            else:
                break

        pnum = int(pnum) - 1
        filename = prob_list[title_list[pnum]] + '.txt'
        Prob = Problem(title_list[pnum])
        vhints, hhints = get_problem(int(prob_list[title_list[pnum]]))
        for clue in hhints:
            new = Clue(tuple(clue))
            Prob.add_clue(new, orient='r')
        for clue in vhints:
            new = Clue(tuple(clue))
            Prob.add_clue(new, orient='c')

    else:
        exit(0)

    os.system('clear')
    Prob.print_problem()

    raw_input("Enter to start... ")

    suc = Prob.solve(v=visual, t=interval)
    os.system('clear')

    if suc:
        answer = Prob.print_problem(char=[' ', '■', ' '])
        print("Done")
        with open('ans_' + filename, 'w') as f:
            f.write(answer)
    else:
        Prob.print_problem()
        print("Fail to solve")

    sel = raw_input("q: Quit\notherwise: Home\n")
    if sel == 'q':
        exit(0)
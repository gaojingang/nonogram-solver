import os
from itertools import combinations_with_replacement
from time import sleep
'''
数图  以 5x5 坐标为例，每个坐标只能出现一个图案，
每一列、每一行的分割数据为  奇数 总行数/2 +1 ,偶数  总行数/2

 0,1,2,3,4
0
1
2
3
4
（x,y)
 sum(x0)  x0 (
 x[] = [[0,3,1],[0,1,1],[0,0,3],[0,0,1],[0,2,1]]
 y[] = [[1,1,1],[0,1,3],[0,0,3],[0,0,1],[0,0,2]]

sum(x0) = x[0][0] + x[0][1] x[0][2]


问题定义
文件头第一行为 矩形 x,y




'''

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
        # def print_problem(self, orient=None, idx=-1, char=['□', '■', ' ']):

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


def test02():
    filename= "problem2.txt"
    prob = Problem(filename)

    with open(filename, "r") as f:
        M, N = map(int, f.readline().split())
        print ("M\t{}".format(M))
        print("N\t{}".format(N))
        for i in range(M):
            line = f.readline()
            print("subM\t{}".format(line.split()))
            # new = Clue(tuple(map(int, f.readline().split())))
            new = tuple(map(int, line.split()))
            # print(new)

            prob.add_clue(new,orient='r')

        #     new = Clue(tuple(map(int, f.readline().split())))
        #     Prob.add_clue(new, orient='r')
        #
        for i in range(N):
            line = f.readline()
            print("subN\t{}".format(line.split()))
            print(tuple(map(int, line.split())))
            new = tuple(map(int, line.split()))
            prob.add_clue(new, orient='c')

        print (prob.RC)
        print(prob.CC)
        # for i in range(N):
        #     new = Clue(tuple(map(int, f.readline().split())))
        #     Prob.add_clue(new, orient='c')

def main():
    visual = False
    interval = 0

    vhints = [[1, 3], [1, 1, 1], [5], [1, 1], [5]]
    hhints = [[5], [1, 1], [3, 1], [1, 1, 1], [5]]

    filename = "problem2.txt"
    Prob = Problem(filename)
    for clue in hhints:
        new = Clue(tuple(clue))
        Prob.add_clue(new, orient='r')
    for clue in vhints:
        new = Clue(tuple(clue))
        Prob.add_clue(new, orient='c')

    Prob.print_problem()

    suc = Prob.solve(v=visual, t=interval)

    suc = Prob.solve(v=visual, t=interval)
    # os.system('clear')

    if suc:
        answer = Prob.print_problem(char=[' ', '■', ' '])
        print("Done")
        with open('ans_' + filename, 'w') as f:
            f.write(answer)
    else:
        Prob.print_problem()
        print("Fail to solve")

if __name__ == '__main__':
    main()
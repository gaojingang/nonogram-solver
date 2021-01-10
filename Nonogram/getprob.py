from urllib import urlopen
import re
import ast


def encode(v):
    idx = 0
    ret = ''
    while idx < len(v):
        if v[idx] == '%':
            c = v[idx+1:idx+3]
            ch = chr(int(c, 16))
            ret += ch
            idx += 3
        else:
            ret += v[idx]
            idx += 1
    return ret


def get_problem(pid):
    # puzzle_num = 11092
    page = urlopen("http://nemonemologic.com/play_logic.php?quid="+str(pid)).read()

    page = page.split('\n')
    data = None
    for line in page:
        if 'data-holder' in line:
            data = line.split()[-1]

    data = encode(data[7:-2])
    p = r"\"([a-zA-Z]+)\":([^\"]+)"
    parse = dict(re.findall(p, data))
    vhints = ast.literal_eval(parse['vhints'].strip(','))
    hhints = ast.literal_eval(parse['hhints'].strip(','))

    return vhints, hhints

def get_prob_list(pagenum, size):
    page = urlopen("http://nemonemologic.com/logic_board.php?page=" + str(pagenum) + "&size="+str(size)).read().split('\n')
    ret = {}
    for line in page:
        if 'quid' in line:
            plist = re.findall('quid=([0-9]+).*>(.*)<.*', line)
            for id, title in plist:
                ret[title] = id
    return ret
# print (page)
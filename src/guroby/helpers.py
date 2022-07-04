import re
from itertools import groupby

def check_lastest_result(result, k):
    if len(result) < k:
        return False
    else:
        results = result[-k:]
        g = groupby(results)
        return next(g, True) and not next(g, False)

def conv2dict(fac, cust, s):

    dic = {}
    for i in range(fac):
        for j in range(cust):
            key = (j, i)
            value = s[2*i+j]
            dic[key] = value

    return dic

def filterDigit(len, model):
    digitList = []
    pattern_one = re.compile(r' \d.\d')
    pattern_two = re.compile(r'-\d.\d')
    for i in range(len):

        s = str(model.getVars()[i])
        mo = pattern_one.search(s)
        if mo == None:
            mo = pattern_two.search(s)

        digitList.append(int(mo.group()[1]))

    return digitList
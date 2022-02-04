from re import compile


def findAllWithRe(data, pattern):
    return compile(pattern).findall(data)


def findAllNumsWithRe(data):
    r = findAllWithRe(data, r'\-?\d+')
    res = []
    for i in r:
        res.append(int(i))
    return res

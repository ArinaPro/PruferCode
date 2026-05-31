
def decoder(code):
    from collections import Counter
    n = len(code) + 2
    code += ''.join(list(map(str, range(1, n + 1))))
    c = dict(Counter(code))
    a = { x: c.get(x) for x in c}

    res = ""

    for el in range(len(a)):
        a_itms = list(a.items())
        a_itms.sort(key = lambda x: (x[1], x[0]))
        res += a_itms[0][0]
        a.pop(a_itms[0][0])
        if code[el] in a.keys():
            a[code[el]] -= 1




    return [res, code]



def encoder(graph):
    pass


# code = input()
# from collections import Counter
# n = len(code)+2
# code += ''.join(list(map(str, range(1, n+1))))
# c = dict(Counter(code))
# a = [(c.get(x), x) for x in c]
#
# a.sort()
# for el in a:
#     print(el[1], end="")
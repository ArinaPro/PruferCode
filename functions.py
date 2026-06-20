from random import randint
from time import time
import heapq
import sympy
from sympy import combinatorics


def decoder(code):
    from collections import Counter
    n = len(code) + 2
    code += ' '.join(list(map(str, range(1, n + 1))))
    c = dict(Counter(code))
    a = {x: c.get(x) for x in c}

    res = ""

    for el in range(len(a)):
        a_itms = list(a.items())
        a_itms.sort(key = lambda x: (x[1], x[0]))
        res += a_itms[0][0]
        a.pop(a_itms[0][0])
        if code[el] in a.keys():
            a[code[el]] -= 1

    return [res, code]


def decode(code):
    str_code = " ".join(code)
    str_tree = decoder(str_code)
    tree = list(str_code[1])
    return tree


# 5 sec for 10_000
def encoder_n2(graph):
    """
    the array of edges (i, j)
    :param graph:
    :return:
    """
    n = max([max(i, j) for (i, j) in graph])
    valences = [0] * (n + 1)
    for (i, j) in graph:
        valences[i] += 1
        valences[j] += 1
    edge_set = [set([i, j]) for (i, j) in graph]
    struct = sorted([(val, ind) for ind, val in enumerate(valences) if ind != 0])
    code = []
    for step in range(n-2):
        parent = 0
        _, i = struct.pop(0)
        for edge in edge_set:
            if i in edge:
                parent = sum(edge) - i
                code.append(parent)
                edge_set.remove(edge)
                break
        valent = [val for val, item in struct if item == parent][0]
        struct.remove((valent, parent))
        struct.append((valent - 1, parent))
        struct.sort()

    return code


# 0.3sec for 100_000
def encodernlogn(graph):
    """
    the array of edges (i, j)
    :param graph:
    :return:
    """
    n = max([max(i, j) for (i, j) in graph])
    code = [0] * (n-2)
    valences = [0] * (n + 1)
    edge_map = {i: set() for i in range(1, n + 1)}
    for (i, j) in graph:
        edge_map[i].add(j)
        edge_map[j].add(i)
        valences[i] += 1
        valences[j] += 1
    heap = [ind for (ind, val) in edge_map.items() if len(val) == 1]
    heapq.heapify(heap)
    for step in range(n-2):
        child = heapq.heappop(heap)
        parent = list(edge_map[child])[0]
        edge_map[parent].remove(child)
        if len(edge_map[parent]) == 1:
            heapq.heappush(heap, parent)
        code[step] = parent
    return code


    # leaves = sorted([(i, j) for (i, j) in graph if valences[i] == 1])


def encoder(graph):
    n = max([max(i, j) for (i, j) in graph])
    code = [0] * (n - 2)
    prev_next = [(i - 1, i + 1) for i in range(0, n + 1)]
    visited = [0] * (n + 1)
    degree = [0] * (n + 1)
    parent = [0] * (n + 1)
    visited[n] = 1
    stack = [n]
    edge = [[] for _ in range(n + 1)]
    for (i, j) in graph:
        edge[i].append(j)
        edge[j].append(i)
        degree[i] += 1
        degree[j] += 1

    while stack:
        u = stack.pop()
        for v in edge[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)

    child = 0
    while degree[child] != 1:
        child += 1

    for step in range(n - 2):
        (prev, next) = prev_next[child]
        if prev > 0:
            prev_next[prev] = (prev_next[prev][0], next)
        if next <= n:
            prev_next[next] = (prev, prev_next[next][1])
        par = parent[child]
        code[step] = par
        degree[par] -= 1
        if degree[par] == 1 and par < child:
            child = par
        else:
            degree[child] -= 1
            while degree[child] != 1:
                child = prev_next[child][1]

    return code

def generate_tree(size):
    tree = []
    start = randint(1, size+1)
    current = [start]
    free = [i for i in range(1, size + 1) if i != start]
    for step in range(size - 1):
        ind_c = randint(0, step)
        ind_f = randint(0, size - step - 2)
        # print(ind_c, ind_f, len(current), len(free))
        c = current[ind_c]
        f = free[ind_f]
        current.append(f)
        free.remove(f)
        tree.append((c, f))
    return tree

def test():
    # size = 1000_000
    graphs = [
        [(1, 4), (4, 3), (2, 3), (5, 3)],
        [(1, 2), (2, 3), (3, 4)],
        [(1, 5), (2, 5), (3, 5), (4, 5)],
    ]
    codes = [
        [4, 3, 3],
        [2, 3],
        [5, 5, 5]
    ]
    # for index, graph in enumerate(graphs):
    #     ans = encodernlogn(graph)
    #     print(ans)
    #     assert(ans == codes[index])
    # for code in codes:
    #     assert(code == encodernlogn(decoder(code)))
    for size in [100, 1000, 10000, 100000]:
        time_start = time()
        tree = generate_tree(size)
        print(f"generated {size} in {round(time() - time_start, 3)} secnds")
        time_start = time()
        encodernlogn(tree)
        print(f"encoded {size} in {round(time() - time_start, 3)} secnds")
        time_start = time()
        sympy.combinatorics.Prufer.to_prufer(tree=tree, n=size)
        print(f"encoded {size} in {round(time() - time_start, 3)} secnds by py library")

test()

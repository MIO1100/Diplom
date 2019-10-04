import subprocess


def f7(seq):
    seen = set()
    seen_add = seen.add
    list.clear()
    return [x for x in seq if not (x in seen or seen_add(x))]




import functools
import math
import statistics
import random


def acronym(list):
    if list:
        return list[0][0] + acronym(list[1:])
    else:
        return ""

print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))


def median(list: list[any]):
    list = sorted(list)
    middle = len(list) // 2
    return (list[middle] + list[middle - 1]) / 2 if len(list) % 2 == 0 else list[len(list) // 2]

l = random.sample(range(100), 100)
print(median(l))
print(statistics.median(l))


def sqrt(x, epsilon):
    if x < 0:
        raise Exception("Square root of Negative number")

    def inner(current):
        return current if abs(current ** 2 - x) < epsilon else inner((current + x / current) / 2)

    return inner(1)

print(sqrt(2, 1e-10))
print(math.sqrt(2))


def make_alpha_dict(s: str):
    words = s.split()
    letters = filter(lambda w: w[0].isalpha(), s)

    d = {x: list(filter(lambda w: x in w, words)) for x in letters}
    return d


print(make_alpha_dict("on i ona"))

def flatten(l: list[any]):
    return [] if not l else (
        flatten(l[0]) + flatten(l[1:]) if isinstance(l[0], list) else [l[0]] + flatten(l[1:])
    )

print(flatten([1, [2, 3], [[4, 5], 6]]))







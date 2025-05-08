def is_even(n):
    return n % 2 == 0

ne = [1, 3, 5, 7, 9]
e = [2, 4, 6, 8, 10]
ene = [1, 2, 3, 4, 5]

def forall(pred, iterable):
    return all(map(pred, iterable))

print("Forall")
print(forall(is_even, ne))
print(forall(is_even, e))
print(forall(is_even, ene))


def exists(pred, iterable):
    return any(map(pred, iterable))

print("Exists")
print(exists(is_even, ne))
print(exists(is_even, e))
print(exists(is_even, ene))


def atleast(n, pred, iterable):
    count = 0
    for x in iterable:
        if pred(x):
            count += 1

        if count >= n:
            return True

    return False

print("Atleast")
print(atleast(2, is_even, ne))
print(atleast(2, is_even, e))
print(atleast(2, is_even, ene))


def atmost(n, pred, iterable):
    count = 0
    for x in iterable:
        if pred(x):
            count += 1

        if count > n:
            return False

    return True

print("Atmost")
print(atmost(2, is_even, ne))
print(atmost(2, is_even, e))
print(atmost(2, is_even, ene))



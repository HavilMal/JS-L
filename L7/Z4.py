from functools import lru_cache, cache


def make_generator(f):
    i = 1
    while True:
        yield f(i)
        i += 1

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    gen = make_generator(fibonacci)

    for i in range(20):
        print(next(gen))

    gen = make_generator(lambda n: n ** 2)
    for i in range(20):
        print(next(gen))

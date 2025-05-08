import time
from Z4 import make_generator, fibonacci
from functools import cache, lru_cache

def make_generator_mem(f):
    fn = cache(f)
    return make_generator(fn)

def slow(n):
    time.sleep(1)
    return n + 1

generator = make_generator_mem(fibonacci)

# for _ in range(100):
#     print(next(generator))

generator = make_generator_mem(slow)
for _ in range(2):
    for _ in range(10):
        print(next(generator))
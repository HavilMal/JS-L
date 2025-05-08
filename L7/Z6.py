import functools
import inspect
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def log(level):
    def decorator(obj):
        if inspect.isfunction(obj):
            def fn_wrapper(*args, **kwargs):
                start = time.time()
                result = obj(*args, **kwargs)
                end = time.time()
                logging.log(level, f"start: {start}, execution: {end - start}s, name: {obj.__name__}, args: {args}, kwargs: {kwargs}, result: {result}")
                return result

            return fn_wrapper

        elif inspect.isclass(obj):
            init = obj.__init__

            def init_wrapper(self, *args, **kwargs):
                result = init(self, *args, **kwargs)
                logging.log(level, f"name: {obj.__name__}, time: {time.time()}, args: {args}, kwargs: {kwargs}")
                return result

            obj.__init__= init_wrapper
            return obj

    return decorator


@log(logging.DEBUG)
def fn(n):
    time.sleep(1)
    print(n)
    return n + 1


print("def")

fn(1)
fn(2)

@log(logging.DEBUG)
class Dummy:
    def __init__(self, n):
        print("from init: ",n)

print("init")

d = Dummy(1)
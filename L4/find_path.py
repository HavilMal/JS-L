import os
import sys
from operator import contains
from os import environ

def contains_substring_from_list(item, li):
    for v in li:
        if v in item:
            return True

    return False

def print_env():
    if len(sys.argv) > 1:
        variables = filter(lambda x: contains_substring_from_list(x, sys.argv[1:]), environ.keys())
    else:
        variables = os.environ.keys()

    for var in sorted(variables):
        print(var, "=", environ[var])




if __name__ == '__main__':
    print_env()
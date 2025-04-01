import os
import sys


def print_path_dir():
    for path in os.environ["PATH"].split(";"):
        if os.path.isdir(path):
            print(path)


def print_path_files():
    for path in os.environ["PATH"].split(";"):
        if os.path.isdir(path):
            print(path)
            for file in os.listdir(path):
                if file.endswith(".exe"):
                    print("\t", file)


def run_option():
    if len(sys.argv) < 1:
        print("No argument entered\nUsage: python print_path.py <dir/file>")
    elif sys.argv[1] == "dir":
        print_path_dir()
    elif sys.argv[1] == "file":
        print_path_files()
    else:
        print(f"Bad argument: {sys.argv[1]}\nUsage: python print_path.py <dir/file>")


if __name__ == "__main__":
    run_option()
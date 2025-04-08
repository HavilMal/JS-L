import collections
import sys

FLAGS = ["--lines", "--follow"]
DEFAULT_LINE_COUNT = 10

def parse_args():
    flags = []
    arguments = []

    for arg in sys.argv[1:]:
        for flag in FLAGS:
            if arg.startswith(flag):
                index = arg.index("=")
                if index != -1:
                    flags.append((flag, arg[index+1:]))
                else:
                    flags.append(tuple(flag))
            else:
                arguments.append(arg)

    return flags, arguments

def get_flag_value(flag_list, flag):
    for f in flag_list:
        if f[0] == flag:
            return f[1]

    return None

def read_last(iterable, lines):
    last = collections.deque(maxlen=lines)
    for line in iterable:
        last.append(line)

    return list(last)

# isatty
# sys.stdin in queue
def run():
    flags, args = parse_args()

    line_count = get_flag_value(flags, "--lines")
    if line_count is None:
        line_count = DEFAULT_LINE_COUNT

    follow = get_flag_value(flags, "--follow")
    if follow is None:
        follow = False







if __name__ == "__main__":
    # read_last(sys.argv[1], sys.argv[2])
    with open("calilneczka.txt") as f:
        lines = read_last(f, 10)
        for i, line in enumerate(lines):
            print(i, "\t", line, end="")

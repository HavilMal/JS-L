import collections
import os
import sys
import time

FLAGS = ["--lines", "--follow"]
DEFAULT_LINE_COUNT = 10
DEFAULTS = {
    "--lines": DEFAULT_LINE_COUNT,
    "--follow": False,
}


def parse_args():
    flags = {}
    arguments = []

    for arg in sys.argv[1:]:
        is_argument = True
        for flag in FLAGS:
            if arg.startswith(flag):
                is_argument = False
                index = arg.find("=")
                if index != -1:
                    flags[flag] = arg[index + 1:]
                else:
                    flags[flag] = True
                break

        if is_argument:
            arguments.append(arg)

    return flags, arguments


def get_flag_value(flag_list, flag):
    if flag in flag_list:
        return flag_list[flag]

    return DEFAULTS[flag]


def read_last(iterable, lines):
    last = collections.deque(maxlen=lines)
    for line in iterable:
        last.append(line)

    for line in last:
        sys.stdout.write(line)
        sys.stdout.flush()


def tail_stream(stream, line_count, follow):
    read_last(stream, line_count)

    while follow:
        line = stream.readline()
        if not line:
            time.sleep(0.1)
        else:
            sys.stdout.write(line)
            sys.stdout.flush()


def tail_file(filename, line_count, follow):
    with open(filename, "r") as file:
        read_last(file, line_count)

        while follow:
            current_position = file.tell()
            line = file.readline()

            if not line:
                time.sleep(0.1)

                current_size = os.stat(filename).st_size

                if current_position > current_size:
                    file.seek(current_size)
            else:
                sys.stdout.write(line)
                sys.stdout.flush()

# isatty
# sys.stdin in queue
def run():
    flags, args = parse_args()
    line_count = int(get_flag_value(flags, "--lines"))
    follow = get_flag_value(flags, "--follow")

    if len(args) > 1:
        raise ValueError("Too many arguments")

    if len(args) == 1:
        tail_file(args[0], line_count, follow)
        return

    if len(args) == 0:
        tail_stream(sys.stdin, line_count, follow)



if __name__ == "__main__":
    run()

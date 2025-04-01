from Utils.read import read_input, find_preamble, read_contents
from Utils.write import write_result

# todo chane
def count_paragraphs(generator):
    count = 0

    contents = read_contents(read_input())
    previous = next(contents)
    line = None

    for line in contents:
        if previous != "\n" and line == "\n":
            count += 1

        previous = line

    # if text ends with text count it too
    if line is not None and line != "\n":
        count += 1


    return count

if __name__ == '__main__':
    write_result(count_paragraphs(read_input()))


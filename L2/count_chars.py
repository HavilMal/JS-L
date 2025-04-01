from Utils.read import read_contents, read_sentence, read_words, read_input
from Utils.write import write_result


def count_chars(generator):
    count = 0
    for line in read_contents(generator):
        for char in line:
            if not char.isspace():
                count += 1

    return count

if __name__ == '__main__':
    write_result(count_chars(read_input()))

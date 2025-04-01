from Utils.read import read_contents, read_sentence, read_non_alfanum, read_input
from Utils.write import write_result


def first_subordinate_clauses(generator):
    for sentence in read_sentence(read_contents(read_input())):
        count = 0
        for char in read_non_alfanum(sentence):
            if char == ",":
                count += 1
            if count > 1:
                return sentence


if __name__ == "__main__":
    write_result(first_subordinate_clauses(read_input()))
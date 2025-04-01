from Utils.read import read_contents, read_sentence, read_input
from Utils.write import write_result


def longest_sentence(generator):
    sentences = read_sentence(read_contents(generator))
    longest = next(sentences)
    length = len(longest)

    for sentence in sentences:
        if len(sentence) > length:
            length = len(sentence)
            longest = sentence

    return longest


if __name__ == '__main__':
    write_result(longest_sentence(read_input()))
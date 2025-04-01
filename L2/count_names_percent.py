from logging import exception

from Utils.read import read_contents, read_sentence, read_words, read_input
from Utils.write import write_result


def count_names_percent(generator) -> float:
    sentences_total = 0
    sentences_with_names = 0

    for sentence in read_sentence(read_contents(generator)):
        sentences_total += 1
        words = read_words(sentence)
        next(words)
        for word in words:
            if word[0].isupper():
                sentences_with_names += 1
                break

    if sentences_total == 0:
        raise Exception("No sentences found")

    return sentences_with_names / sentences_total * 100


if __name__ == '__main__':
    write_result(count_names_percent(read_input()))

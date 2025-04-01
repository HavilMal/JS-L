from Utils.read import read_contents, read_sentence, read_words, read_non_alfanum, read_input
from Utils.write import write_results


def question_or_exclamation(generator):
    for sentence in read_sentence(read_contents(generator)):
        if sentence[-1] == "?" or sentence[-1] == "!":
            yield sentence


if __name__ == "__main__":
    write_results(question_or_exclamation())


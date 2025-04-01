from Utils.read import read_contents, read_sentence, read_words, read_non_alfanum, read_input
from Utils.write import write_results


def first_20_sentences(generator):
    for i, sentence in enumerate(read_sentence(generator)):
        if i < 20:
            yield sentence
        else:
            return


if __name__ == '__main__':
    write_results(first_20_sentences(read_input()))
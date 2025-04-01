from Utils.read import read_contents, read_sentence, read_words, read_input
from Utils.write import write_results


def sentence_4_words(generator):
    for sentence in read_sentence(read_contents(generator)):
        count = 0
        for word in read_words(sentence):
            count += 1
            if count > 4:
                break

        if count <= 4:
            yield sentence


if __name__ == "__main__":
    write_results(sentence_4_words(read_input()))
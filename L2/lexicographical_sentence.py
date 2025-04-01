from Utils.read import read_contents, read_sentence, read_words, read_non_alfanum, read_input
from Utils.write import write_results


def is_lexicographical(sentence):
    words = read_words(sentence)
    previous = next(words).lower()

    for word in words:
        if not (word.lower() > previous):
            return False
        previous = word.lower()

    return True

def lexicographical_sentence(generator):
    for sentence in read_sentence(read_contents()):
        if is_lexicographical(sentence):
            yield sentence


if __name__ == "__main__":
    write_results(lexicographical_sentence(read_input()))

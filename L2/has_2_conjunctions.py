from Utils.read import read_contents, read_sentence, read_words, read_input
from Utils.write import write_results


def has_2_conjunctions(generator):
    for sentence in read_sentence(read_contents()):
        count = 0
        for word in read_words(sentence):
            if word == "i" or word == "oraz" or word == "ale" or word == "że" or word == "lub":
                count += 1

            if count >= 2:
                yield sentence
                break

if __name__ == "__main__":
    write_results(has_2_conjunctions(read_input()))
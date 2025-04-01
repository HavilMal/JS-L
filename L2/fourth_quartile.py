from Utils.read import read_contents, read_sentence, read_words, read_non_alfanum, read_input
from Utils.write import write_results


def fourth_quartile(generator):
    lengths = []

    for sentence in read_sentence(read_contents(generator)):
        lengths.append((len(sentence), sentence))

    lengths.sort(key=lambda x: x[0])

    third_quartile = int(len(lengths) * 0.75)
    for i in range(third_quartile, len(lengths)):
        yield lengths[i][1]


if __name__ == "__main__":
    write_results(fourth_quartile(read_input()))

    



from Utils.read import read_contents, read_sentence, read_words, read_input
from Utils.write import write_result


# neighbouring words
def has_words_starting_with_same_letter(sentence):
    words = read_words(sentence)
    previous = next(words)[0].lower()

    for word in words:
        if word[0].lower() == previous:
            return True

        previous = word[0].lower()

    return False

def longest_sentence(generator):
    longest = None
    length = 0

    for sentence in read_sentence(read_contents(generator)):
        if not has_words_starting_with_same_letter(sentence):
            if len(sentence) > length:
                longest = sentence
                length = len(sentence)

    return longest

if __name__ == "__main__":
    write_result(longest_sentence(read_input()))
import io
import sys
from os import SEEK_SET
from typing import Generator, Any


def read_input() -> io.TextIOWrapper:
    # wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    # return wrapper
    sys.stdin.reconfigure(encoding='utf-8')
    return sys.stdin


def find_preamble(generator) ->  str:
    contents = ""
    lines = 0
    previous_new_line = False

    for line in generator:
        if lines > 10:
            return contents
        else:
            lines += 1

        if previous_new_line and line == "\n":
            return ""

        previous_new_line = line == "\n"
        contents = contents + line

    return contents


def read_contents(buffer) -> Generator[str, Any, None]:
    contents = find_preamble(buffer)

    if contents != "":
        yield contents

    for line in buffer:
        if line.startswith("-----"):
            return

        yield line


def read_sentence(generator) -> Generator[str, Any, None]:
    sentence = ""
    for line in generator:
        for char in line:
            if not (sentence == "" and char == " "):
                if not (char.isspace() and char != " "):
                    sentence += char

            if char == "." or char == "!" or char == "?":
                yield sentence
                sentence = ""


def read_words(generator) -> Generator[str, Any, None]:
    word = ""
    for char in generator:
        if char.isalpha():
            word += char
        elif word != "":
            yield word
            word = ""


def read_non_alfanum(generator) -> Generator[str, Any, None]:
    for char in generator:
        if not (char.isalpha() or char.isdigit() or char.isspace()):
            yield char

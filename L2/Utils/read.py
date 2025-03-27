import io
import sys


def readInput() -> str:
    text = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8').read()
    return text


def findPreambleEnd(input: str) -> int:
    index = input.find("\n\n")
    if index > 10 or index == -1:
        return 0
    else:
        return index

def findPublisherStart(input: str) -> int:
    index = input.find("-----")
    if index > 10 or index == -1:
        return 0
    else:
        return index

def stripContents(input: str):
    return input[findPreambleEnd(input):][:findPublisherStart(input)]

print(stripContents(readInput()))
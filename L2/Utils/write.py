import io
import sys
from typing import Generator, Any


def write_result(result) -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdout.write(str(result) + "\n")
    sys.stdout.flush()

def write_results(results: Generator[str, Any, None]) -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    for line in results:
        sys.stdout.write(line + "\n")

    sys.stdout.flush()


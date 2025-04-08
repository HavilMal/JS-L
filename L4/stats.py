import json
import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess


def run(dir_path):
    files = []
    for path in Path(dir_path).iterdir():
        if path.is_file():
            result: CompletedProcess[str] = subprocess.run(["L4-R.exe", str(path)], capture_output=True, text=True)
            if result.stdout:
                j = json.loads(result.stdout)
                files.append(j)

    sys.stdout.write(f"Files processed: {len(files)}\n")
    sys.stdout.write(f"Total characters: {sum(map(lambda x: x["char_count"], files))}\n")
    sys.stdout.write(f"Total words: {sum(map(lambda x: x["word_count"], files))}\n")
    sys.stdout.write(f"Most common character: {max(files, key=lambda x: x["most_common_word_count"])["most_common_char"]}\n")
    sys.stdout.write(f"Most common word: {max(files, key=lambda x: x["most_common_word_count"])["most_common_word"]}\n")

    sys.stdout.flush()



if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
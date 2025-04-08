import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_CONVERTED_DIR = "converted"
DEFAULT_HISTORY_FILE = "history.csv"

AUDIOVIDEO_EXTENSIONS = ('mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'flac')
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico', 'svg', 'heic')

def get_args():
    return sys.argv[1:]

def get_converted_dir():
    if "CONVERTED_DIR" in os.environ:
        return Path(os.environ["CONVERTED_DIR"]).absolute()

    return Path(DEFAULT_CONVERTED_DIR).absolute()

def create_converted_dir():
    if not get_converted_dir().exists():
        os.mkdir(get_converted_dir())


def save_log(original_path: Path, format: str, output_path: Path, program):
    logfile = os.path.join(get_converted_dir(), DEFAULT_HISTORY_FILE)
    create_converted_dir()

    if not Path(logfile).exists():
        try:
            open(logfile, "x")
        except OSError as e:
            raise Exception("Cant create log file: {}".format(logfile), e)

    with open(logfile, "a+") as f:
        f.write(f"{str(datetime.now())},{str(original_path)},{format},{str(output_path)},{str(program)}\n")


def is_audiovideo(file):
    return Path(file).suffix.replace(".", "") in AUDIOVIDEO_EXTENSIONS

def is_image(file):
    return Path(file).suffix.replace(".", "") in IMAGE_EXTENSIONS


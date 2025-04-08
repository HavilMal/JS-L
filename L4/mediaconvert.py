import datetime
import subprocess
import argparse
from pathlib import Path

import filetype

import utils
from utils import get_args, get_converted_dir, save_log, AUDIOVIDEO_EXTENSIONS, IMAGE_EXTENSIONS


def convert_audiovisual(path, format):
    input_path = Path(path).absolute()
    time = datetime.datetime.now().strftime('%Y%m%d')
    output_path = get_converted_dir() / f"{time}-{input_path.stem}.{format.replace(".", "")}"

    save_log(input_path, format, output_path, "ffmpeg")
    subprocess.run(["ffmpeg", "-i", input_path, output_path])


def convert_image(path, format):
    input_path = Path(path).absolute()
    time = datetime.datetime.now().strftime('%Y%m%d')
    output_path = get_converted_dir() / f"{time}-{input_path.stem}.{format.replace(".", "")}"

    save_log(input_path, format, output_path, "magic")
    subprocess.run(["magick", input_path, output_path])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--video", type=str)
    parser.add_argument("--image", type=str)

    args = parser.parse_args()

    folder = Path(args.folder)

    if not args.video and not args.image:
        raise Exception("Error: Please specify either --video <format> or --image flag.")

    if not folder.is_dir():
        raise ValueError("Enter valid path to directory to convert.")

    if args.video and args.video not in AUDIOVIDEO_EXTENSIONS:
        raise Exception(f"Unknown video format: {args.video}")

    if args.image and args.image not in IMAGE_EXTENSIONS:
        raise Exception(f"Unknown image format: {args.image}")

    for path in folder.iterdir():
        if path.is_file():
            if args.video and utils.is_audiovideo(path):
                convert_audiovisual(path, args.video)
            elif args.image and utils.is_image(path):
                print(path)
                convert_image(path, args.image)



if __name__ == "__main__":
    main()


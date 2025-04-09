import re
from pathlib import Path

def group_measurement_files_by_key(path: Path):
    measurements_dict = {}
    for file in path.iterdir():
        if file.is_file():
            filename = re.match(r"^(?P<year>[^_]+)_(?P<measurement>.+)_(?P<frequency>.+)\.csv$", file.name)

            if not filename:
                raise Exception(f"File name: {file.name} is not a valid filename")

            year = filename.group("year")
            measurement = filename.group("measurement")
            frequency = filename.group("frequency")

            measurements_dict[(year, measurement, frequency)] = file

    return measurements_dict


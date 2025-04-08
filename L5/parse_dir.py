import re
from pathlib import Path

def group_measurement_files_by_key(path: Path):
    measurements_dict = {}
    for file in path.iterdir():
        if file.is_file() and re.match(r"\w+(?=\.csv)", file.name):
            year = re.search(r"^\d{4}", file.name).group()
            measurement = re.search(r"(?<=^\d{4}_)[a-zA-Z0-9_]+(?=_[0-9]+[gm]\.csv)", file.name).group()
            frequency = re.search(r"[0-9]+[gm](?=.csv)", file.name).group()

            measurements_dict[(year, measurement, frequency)] = file

    print(measurements_dict)


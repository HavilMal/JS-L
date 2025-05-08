import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List

from station import SeriesValidator, TimeSeries


class Measurements:
    def __init__(self, path: Path):
        self.path = path
        if not path.is_dir():
            raise Exception(f"Path {path} is not a directory")

        self.loaded = []
        self.loaded_paths = []


    def __len__(self):
        self.load_all()
        return len(self.loaded)

    def __contains__(self, item):
        return item in [timeseries.measurement_name for timeseries in self.loaded]

    def get_by_parameter(self, parameter_name:str):
        return list(filter(lambda x: x.measurement_name == parameter_name, self.loaded))

    def get_by_station(self, station_code:str):
        return list(filter(lambda x: x.station_code == station_code, self.loaded))

    def detect_all_anomalies(self, validators: List[SeriesValidator], preload: bool = False):
        if preload:
            self.load_all()

        anomalies = []

        for validator in validators:
            for series in self.loaded:
                anomalies.append(validator.analyze(series))


    def _read_info_lines(self, reader):
        field_names = ["No", "codes", "measurements", "average_times", "units", "stand_codes"]
        fields = {}

        data_offset = 1

        for key in field_names:
            values = next(reader)
            if values[0] == "":
                data_offset = 2
            fields[key] = values[data_offset:]

        stations = []


        for i in range(len(fields["codes"])):
            stations.append(
                TimeSeries(fields["measurements"][i], fields["codes"][i], fields["average_times"][i], [], [], fields["units"][i])
            )

        return stations, data_offset

    def load(self, path: Path):
        if path in self.loaded_paths:
            return

        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)

            series, data_offset = self._read_info_lines(reader)


            for row in reader:
                date = re.match(r"(\d{2})/(\d{2})/(\d{2})\s(\d{2}):(\d{2})", row[0])
                if date is None:
                    continue

                day = int(date.group(2))
                month = int(date.group(1))
                year = int(date.group(3)) + 2000
                hour = int(date.group(4))
                minute = int(date.group(5))


                for i, value in enumerate(row[data_offset:]):
                    if value:
                        series[i].values.append(float(value))
                        series[i].dates.append(datetime(year, month, day, hour, minute))


            self.loaded_paths.append(path)
            self.loaded += series


    def load_all(self):
        for filename in self.path.glob("*.csv"):
            self.load(filename)







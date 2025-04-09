import csv
import logging
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Self, Dict, NamedTuple

# does not work for:
# 2023_Depozycja_1m.csv
# 2023_NO2_1g.csv

@dataclass
class StationMeasurement:
    code: str
    measurement: str
    average_time: str
    units: str
    stand_code: str
    values: List[float] = field(default_factory=list)


@dataclass
class Measurement:
    name: str
    timestamps: List[str] = field(default_factory=list)
    stations: Dict[str, StationMeasurement] = field(default_factory=dict)



@dataclass
class Station:
    code: str
    international_code: str
    name: str
    old_code: str
    launch_date: str
    closing_date: str
    station_type: str
    area_type: str
    station_kind: str
    voivodeship: str
    town: str
    address: str
    latitude: str
    longitude: str


def read_line_wrapper(readable):
    total_bytes = 0
    for line in readable:
        total_bytes += sum(map(lambda x: len(x.encode("utf-8")), line)) + len(line) - 1
        logging.debug(f"Number of bytes read: {total_bytes}")
        yield line


def _read_info_lines(reader):
    field_names = ["No", "codes", "measurements", "average_times", "units", "stand_codes"]
    fields = {}

    for key in field_names:
        values = next(reader)
        fields[key] = values[1:]

    stations = []

    for i in range(len(fields["codes"])):
        stations.append(
            StationMeasurement(fields["codes"][i], fields["measurements"][i], fields["average_times"][i], fields["units"][i],
                               fields["stand_codes"][i]))

    return stations

def parse_measurement(path: Path) -> Measurement:
    with open(path, newline='') as csvfile:
        logging.info(f"Opened {path}")
        reader = csv.reader(csvfile)

        reader = read_line_wrapper(reader)

        stations = _read_info_lines(reader)
        timestamps = []

        for row in reader:
            timestamps.append(row[0])

            for i, value in enumerate(row[1:]):
                if value:
                    stations[i].values.append(float(value))
                else:
                    stations[i].values.append(None)

    logging.info(f"Closed {path}")
    stations = { s.code: s  for s in stations }
    return Measurement(path.stem, timestamps, stations)


def parse_stations(path: Path) -> Dict[str, Station]:
    stations = {}
    with open(path, newline="", encoding="utf-8") as csvfile:
        logging.info(f"Opened {path}")
        reader = csv.reader(csvfile)
        reader = read_line_wrapper(reader)

        next(reader)

        for row in reader:
            if len(row) != 15:
                raise ValueError("Station row must have 15 fields")

            args = row[1:]

            if args[0] in stations.keys():
                warnings.warn(f"Station {args[0]} already exists")

            stations[args[0]] = Station(*args)

    logging.info(f"Closed {path}")
    return stations

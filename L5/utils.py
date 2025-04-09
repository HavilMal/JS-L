import re
import statistics
import datetime
from pathlib import Path
import random
from typing import Match, List, Dict

from parse_csv import parse_stations, Station, Measurement, StationMeasurement, parse_measurement


def get_measurement(year, measurement, frequency) -> Measurement | None:
    path = Path("measurements") / f"{year}_{measurement}_{frequency}.csv"
    if path.exists():
        return parse_measurement(path)
    else:
        return None


def convert_timestamps(measurement: Measurement):
    timestamps = []
    for timestamp in measurement.timestamps:
        date_groups = re.match(r"(\d{2})/(\d{2})/(\d{2})", timestamp)

        month = int(date_groups.group(1))
        day = int(date_groups.group(2))
        year = int(date_groups.group(3))
        if year < 100:
            year += 2000

        timestamps.append(datetime.datetime(year, month, day))

    return timestamps


def convert_date(date: str, delimiter: str = "-"):
    date_groups = re.match(r"(\d{4})" + delimiter + r"(\d{2})" + delimiter + r"(\d{2})", date)

    if date_groups is None:
        return None

    year = int(date_groups.group(1))
    if year < 100:
        year += 2000
    month = int(date_groups.group(2))
    day = int(date_groups.group(3))

    return datetime.datetime(year, month, day)


def get_range(measurement, start_date, end_date):
    if start_date > end_date:
        raise ValueError(f"Start date ({start_date}) must be before end date ({end_date})")

    timestamps = convert_timestamps(measurement)

    start_index = 0
    found_start = False
    end_index = len(timestamps) - 1

    for i, timestamp in enumerate(timestamps):
        if timestamp >= start_date and not found_start:
            start_index = i + 1
            found_start = True

        if timestamp > end_date:
            end_index = i
            break

    return start_index , end_index

def get_random_station(measurement: Measurement, start_index, end_index) -> StationMeasurement | None:
    stations = measurement.stations
    to_try = set(stations.keys())

    while len(to_try):
        key = random.choice(list(to_try))

        for value in stations[key].values[start_index:end_index]:
            if value is not None:
                return stations[key]

        to_try -= key

    return None


def calculate_average_and_std(measurement: Measurement, station: str, start_index, end_index) -> (float, float):
    if station not in measurement.stations:
        raise Exception(f"Station {station} not in measurements")

    values = measurement.stations[station].values[start_index:end_index]

    valid_values = list(filter(lambda value: value is not None, values))

    try:
        return statistics.mean(valid_values), statistics.stdev(valid_values)
    except statistics.StatisticsError:
        return None, None

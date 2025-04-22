import csv
import statistics
from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class Station:
    def __init__(self, code: str, international_code: str, name: str, old_code: str, launch_date: str,
                 closing_date: str, station_type: str, area_type: str, station_kind: str, voivodeship: str, town: str,
                 address: str, latitude: str, longitude: str):
        self.code = code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.launch_date = launch_date
        self.closing_date = closing_date
        self.station_type = station_type
        self.area = area_type
        self.station_kind = station_kind
        self.voivodeship = voivodeship
        self.town = town
        self.address = address

    def __str__(self):
        return f"Station(code: {self.code}, name: {self.name}, type: {self.station_type}, kind: {self.station_kind}, voivodeship: {self.voivodeship}, town: {self.town}, address: {self.address})"

    def __repr__(self):
        return f"Station(code: {self.code}, internationa_code: {self.international_code}, name: {self.name}, old_code: {self.old_code}, launch_date: {self.launch_date}, closing_date: {self.closing_date}, type: {self.station_type}, area: {self.area}, station_kind: {self.station_kind}, voivodeship: {self.voivodeship}, town: {self.town}, address: {self.address})"

    def __eq__(self, other):
        return self.code == other.code


def parse_stations(path: Path) -> Dict[str, Station]:
    stations = {}
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        next(reader)

        for row in reader:
            if len(row) != 15:
                raise ValueError("Station row must have 15 fields")

            args = row[1:]

            stations[args[0]] = Station(*args)

    return stations


class TimeSeries:
    def __init__(self, measurement_name: str, station_code: str, average_time: str, dates: List[datetime],
                 values: List[float], unit: str):
        self.measurement_name: str = measurement_name
        self.station_code: str = station_code
        self.average_time: str = average_time
        self.dates: List[datetime] = dates
        self.values: List[float] = values
        self.unit: str = unit

    @property
    def average(self):
        if self.values:
            return sum(self.values) / len(self.values)
        else:
            return None

    @property
    def stddev(self):
        if self.values:
            return statistics.stdev(self.values)
        else:
            return None

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.dates[item], self.values[item]
        elif isinstance(item, slice):
            return self.__getitem__(item)
        elif isinstance(item, datetime):
            try:
                index = self.dates.index(item)
            except ValueError:
                raise KeyError(f"{item} is not in dates")

            return self.dates[index], self.values[index]

    def __get_slice(self, slice):
        result = []

        for i in range(slice.start, slice.stop, slice.step):
            result.append((self.dates[slice], self.values[slice]))

        if len(result) == 1:
            return result[0]
        else:
            return result


class SeriesValidator(ABC):
    def analyze(self, series: TimeSeries) -> List[str]:
        pass

    def predicate(self, value):
        pass


class OutlierDetector(SeriesValidator):
    # todo raise exception when k < 0
    def __init__(self, k: int):
        self.k = k

    def analyze(self, series: TimeSeries) -> List[str]:
        return list(filter(lambda x: x is not None, self._analyze(series)))

    def _analyze(self, series: TimeSeries):
        stddev = series.stddev

        if stddev is None:
            return

        threshold = stddev * self.k

        for i, value in enumerate(series.values):
            if abs(value - series.average) > threshold:
                yield f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} deviates from average by {abs(value - series.average)}"
            else:
                yield None


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> List[str]:
        return list(filter(lambda x: x is not None, self._analyze(series)))

    def _analyze(self, series: TimeSeries):
        count = 0

        for i, value in enumerate(series.values):
            if not value:
                count += 1

            if value and count >= 3:
                count = 0
                yield f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} is third non-data value"
            else:
                yield None


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> List[str]:
        return list(filter(lambda x: x is not None, self._analyze(series)))

    def _analyze(self, series: TimeSeries):
        for i, value in enumerate(series.values):
            if value > self.threshold:
                yield f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} is over the threshold by {value - self.threshold}"
            else:
                yield None


class CompositeDetector(SeriesValidator):
    def __init__(self, conjunctive=False, *args):
        self.detectors = list(filter(lambda x: isinstance(x, SeriesValidator), args))
        self.conjunctive = conjunctive

    def analyze(self, series: TimeSeries) -> List[str]:
        if not self.detectors:
            return []

        messages = []

        analyzers = [x._analyze(series) for x in self.detectors]

        for _ in range(len(series.values)):
            result = [next(x) for x in analyzers]

            if self.conjunctive and None not in result:
                messages += result
            else:
                messages += list(filter(lambda x: x is not None, result))

        return messages

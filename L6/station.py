import statistics
from datetime import datetime
from typing import List


class Station:
    def __init__(self):
        ...

    def __str__(self):
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...


class TimeSeries:
    def __init__(self, measurement_name: str, station_code: str, average_time: str, dates: List[datetime], values: List[float], unit: str):
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


class SeriesValidator:
    def analyze(self, series: TimeSeries) -> List[str]:
        pass

    def predicate(self, value):
        pass

class OutlierDetector(SeriesValidator):
    # todo raise exception when k < 0
    def __init__(self, k: int):
        self.k = k

    def analyze(self, series: TimeSeries) -> List[str]:
        stddev = series.stddev

        if stddev is None:
            return []

        threshold = stddev * self.k
        result = []

        for i, value in enumerate(series.values):
            if abs(value - series.average) > threshold:
                result.append(f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} deviates from average by {abs(value - series.average)}")

        return result

class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> List[str]:
        count = 0
        result = []

        for i, value in enumerate(series.values):
            if not value:
                count += 1

            if count >= 3:
                count = 0
                result.append(f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} is third non-data value")

        return result


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> List[str]:
        result = []

        for i, value in enumerate(series.values):
            if self.predicate(value):
                result.append(f"Value {value} measured at {series.dates[i].strftime('%m/%d/%Y')} is over the threshold by {value - self.threshold}")

        return result

    def predicate(self, value):
        return value > self.threshold


class CompositeDetector(SeriesValidator):
    def __init__(self, conjunctive=False,  *args):
        self.detectors = list(filter(lambda x: isinstance(x, SeriesValidator), args))

    def analyze(self, series: TimeSeries) -> List[str]:
        result = []

        for detector in self.detectors:
            result += detector.analyze(series)

        return result






t = TimeSeries("NO2", "Station", "1g", [datetime(1990, 8, 20)], [12], "cm")



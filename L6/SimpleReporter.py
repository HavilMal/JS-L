import statistics
from pathlib import Path

from Measurements import Measurements
from station import TimeSeries, OutlierDetector, ZeroSpikeDetector, ThresholdDetector


class SimpleReporter:
    def analyze(self, series: TimeSeries):
        return [f"Info: {series.measurement_name} at {series.station_code} has mean = {statistics.mean(series.values)}"]


if __name__ == "__main__":
    validators = [OutlierDetector(10), ZeroSpikeDetector(), ThresholdDetector(10), SimpleReporter()]

    me = Measurements(Path("measurements"))
    me.load_all()

    timeseries = me.get_by_parameter("PM10")
    series = timeseries[0]

    for validator in validators:
        print(validator.analyze(series))
from collections import namedtuple

from find import get_address
from parse_csv import *
from parse_dir import group_measurement_files_by_key

# stations = parse_stations("stacje.csv")
# # measurement = parse_measurement(Path("measurements/2023_SO2_1g.csv"))
#
# # print(measurement)
# print(stations)

# group_measurement_files_by_key(Path("measurements"))
get_address(Path("stacje.csv"), "Wrocław")
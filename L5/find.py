import re
from pathlib import Path

from parse_csv import parse_stations


def get_address(path: Path, city: str):
    stations = parse_stations(path)

    matching = []

    for station in stations.values():
        if station.town == city:
            street = re.search(r"^[^\d\\]+", station.address)
            # street = re.search(r".+(?=(\s\d{1,3}\s*\D*(\s|/|-|)\d{0,3}$))|^[^\d]+$", street.group())
            street = re.search(r".+(\s\d{1,3}([a-zA-Z])?((/|\s|-)\d{1,3})*$)", station.address)
            # ".+(\s)(?!(\d{1,3}))"
            number = re.search(r"(\s)[\d\s//-a-zA-Z]+$", station.address)

            print(station.address)

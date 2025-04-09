from pathlib import Path
import re
from typing import Dict, List

from parse_csv import Station, parse_stations


def parse_address(station: Station):
    voivodeship = station.voivodeship.capitalize()
    town = station.town.capitalize()

    if station.address is None:
        return voivodeship, town, None, None

    address = re.match(r"(.+)(\s\d{1,3}([a-zA-Z])?((/|\s|-)\d{1,3})?$)", station.address)

    if address:
        street = address.group(1)
        number = address.group(2)
    else:
        street = station.address
        number = None

    return voivodeship, town, street, number


def get_address(path: Path, city: str):
    stations = parse_stations(path)

    return list(map(parse_address, filter(lambda station: station.town == city, stations.values())))


def find_launch_dates(stations: Dict[str, Station]):
    matching = []
    for station in stations.values():
        date = re.match(r"\d{4}-\d{2}-\d{2}", station.launch_date)
        if date is not None:
            matching.append(station.launch_date)

    return matching


def find_closing_dates(stations: Dict[str, Station]):
    matching = []
    for station in stations.values():
        date = re.match(r"\d{4}-\d{2}-\d{2}", station.closing_date)
        if date is not None:
            matching.append(station.closing_date)

    return matching


def find_coordinates(stations: Dict[str, Station]):
    matching = []
    for station in stations.values():
        latitude = re.match(r"\d+\.\d{6}", station.latitude)
        longitude = re.match(r"\d+\.\d{6}", station.longitude)
        if latitude is not None and longitude is not None:
            matching.append((latitude.group(), longitude.group()))
        elif latitude is None != longitude is None:
            raise Exception(f"Coordinates invalid: {station}")

    return matching


def find_dash_station_names(stations: Dict[str, Station]):
    matching = []
    for station in stations.values():
        name = re.match(r"[^-]+-.+", station.name)
        if name is not None:
            matching.append(name.group())

    return matching


def format_station_names(stations: Dict[str, Station]) -> Dict[str, Station]:
    def replace(c: Match):
        return "acelnoszzACELNOSZZ"["ąćęłńóśźżĄĆĘŁŃÓŚŹŻ".find(c.group())]

    for station in stations.values():
        station.name = re.sub(r"\s", "_", station.name)
        station.name = re.sub(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", replace, station.name)

    return stations


def validate_mobile(stations: Dict[str, Station]) -> List[Station]:
    invalid_mobile_stations = []
    for station in stations.values():
        is_mobile = re.match(r".*MOB", station.code)
        if is_mobile is not None and station.station_kind != "mobilna":
            invalid_mobile_stations.append(station)

    return invalid_mobile_stations


def three_hyphens_localization(stations: Dict[str, Station]):
    matching = []
    for station in stations.values():
        localization = f"{station.voivodeship} {station.town} {station.address}"
        m = re.match(r".+-.+-.+", localization)

        if m is not None:
            matching.append(localization)


def al_or_ul_and_comma_address(stations: Dict[str, Station]):
    return list(filter(lambda station: re.match(r"(al\.|ul\.).*,.*", station.address) is not None, stations.values()))

import argparse
import logging
from pathlib import Path
import click

from parse_csv import parse_stations
from utils import get_random_station, convert_date, get_measurement, calculate_average_and_std, get_range


def run_average(station, measurement_name, frequency, start_date, end_date):
    measurement = get_measurement(start_date.year, measurement_name, frequency)

    if not measurement:
        logging.warning(f"Measurement with given parameters not found")
        return

    start_index, end_index = get_range(measurement, start_date, end_date)

    average, stddev = calculate_average_and_std(measurement, station, start_index, end_index)

    if average is None or stddev is None:
        logging.warning(f"No measurements were taken within given timerange")
        return

    print(f"Average: {average} | Standard Deviation: {stddev}")


def run_random(measurement_name, frequency, start_date, end_date):
    measurement = get_measurement(start_date.year, measurement_name, frequency)

    if not measurement:
        logging.warning(f"Measurement with given parameters not found")
        return

    stations = parse_stations(Path("stacje.csv"))

    start_index, end_index = get_range(measurement, start_date, end_date)

    station_code = get_random_station(measurement, start_index, end_index).code

    if station_code is None:
        logging.warning(f"Random station within given timerange not found")
        return

    station = stations[station_code]

    print(f"Station: {station.name} | Address: {station.town} {station.address}")


def run():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subcommand")

    parser.add_argument("measurement", help="Measurement type (eg. NO2)")
    parser.add_argument("frequency", help="Measurement Frequency (1m/1g/24g)")
    parser.add_argument("start", help="Start of time range (eg. 10-04-2020)")
    parser.add_argument("end", help="End of time range (eg. 10-04-2020)")

    random_parser = subparsers.add_parser("random")
    average_parser = subparsers.add_parser("average")
    average_parser.add_argument("station", help="Station code")


    args = parser.parse_args()

    start_date = convert_date(args.start)
    if start_date is None:
        logging.error(f"Invalid start date: {args.start} (enter: YYYY-MM-DD)")
        return

    end_date = convert_date(args.end)
    if end_date is None:
        logging.error(f"Invalid end date: {args.end} (enter: YYYY-MM-DD)")
        return

    if start_date > end_date:
        logging.error(f"Start date ({start_date}) must be before end date ({end_date})")
        return

    if args.subcommand == "random":
        run_random(args.measurement, args.frequency, start_date, end_date)
    elif args.subcommand == "average":
        run_average(args.station, args.measurement, args.frequency, start_date, end_date)
    else:
        raise Exception("Unknown subcommand")


def validate_dates(start, end):
    start_date = convert_date(start)
    if start_date is None:
        logging.error(f"Invalid start date: {start} (enter: YYYY-MM-DD)")
        return None, None

    end_date = convert_date(end)
    if end_date is None:
        logging.error(f"Invalid end date: {end} (enter: YYYY-MM-DD)")
        return None, None

    if start_date > end_date:
        logging.error(f"Start date ({start_date}) must be before end date ({end_date})")
        return  None, None

    return start_date, end_date

@click.group()
@click.argument("measurement")
@click.argument("frequency")
@click.argument("start")
@click.argument("end")
@click.pass_context
def cli(ctx, measurement, frequency, start, end):
    ctx.ensure_object(dict)
    ctx.obj["measurement"] = measurement
    ctx.obj["frequency"] = frequency
    ctx.obj["start"] = start
    ctx.obj["end"] = end

@cli.command()
@click.argument("station")
@click.pass_context
def average(ctx, station):
    start = ctx.obj["start"]
    end = ctx.obj["end"]

    start_date, end_date = validate_dates(start, end)

    if start_date is None or end_date is None:
        return

    run_average(station, ctx.obj["measurement"], ctx.obj["frequency"], start_date, end_date)

@cli.command()
@click.pass_context
def random(ctx):
    start = ctx.obj["start"]
    end = ctx.obj["end"]

    start_date, end_date = validate_dates(start, end)

    if start_date is None or end_date is None:
        return

    run_random(ctx.obj["measurement"], ctx.obj["frequency"], start_date, end_date)

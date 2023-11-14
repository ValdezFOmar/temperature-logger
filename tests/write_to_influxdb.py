#!/usr/bin/env python

"""InfluxDB testing"""

import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from post_readings import fake_data_multiple_dates


def data_dict_to_points(data: dict):
    readings = data["readings"]
    date = data["date"]

    for reading in readings:
        time_field = reading["time"]
        _time = datetime(
            **date,
            hour=time_field["hour"],
            minute=time_field["minutes"],
            second=time_field["seconds"]
        )
        yield (
            Point("weather")
            .tag("location", "Tijuana")
            .field("temperature", reading["temperature"])
            .time(_time)
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--insert", "-i", action="store_true", help="Insert data")
    group.add_argument(
        "--delete", "-d", action="store_true", help="Delete all the data"
    )
    args = parser.parse_args()

    load_dotenv()
    URL = os.environ["INFLUX_URL"]
    ORG = os.environ["INFLUX_ORG"]
    TOKEN = os.environ["INFLUX_TOKEN"]
    BUCKET = os.environ["INFLUX_BUCKET"]

    test_data = fake_data_multiple_dates(4)
    point_series = (data_dict_to_points(reading) for reading in test_data)

    with InfluxDBClient(url=URL, org=ORG, token=TOKEN, debug=True) as client:
        with client.write_api(write_options=ASYNCHRONOUS) as write_api:
            if args.insert:
                for series in point_series:
                    write_api.write(BUCKET, ORG, series)
            elif args.delete:
                delete_api = client.delete_api()
                delete_api.delete(
                    start=datetime(1970, 1, 1),
                    stop=datetime.now(),
                    predicate='_measurement="weather"',
                    bucket=BUCKET,
                )


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import os

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from post_readings import fake_data_multiple_dates


def data_dict_to_points(data: dict):
    readings = data["readings"]

    points = (
        Point("weather")
        .tag("location", "Tijuana")
        .field("temperature", reading["temperature"])
        for reading in readings
    )
    return points


def main():
    load_dotenv()
    URL = os.environ["INFLUX_URL"]
    ORG = os.environ["INFLUX_ORG"]
    TOKEN = os.environ["INFLUX_TOKEN"]
    BUCKET = os.environ["INFLUX_BUCKET"]

    test_data = fake_data_multiple_dates(1, 1)
    point_series = (data_dict_to_points(reading) for reading in test_data)

    with InfluxDBClient(url=URL, org=ORG, token=TOKEN, debug=True) as client:
        with client.write_api(write_options=ASYNCHRONOUS) as write_api:
            for series in point_series:
                for point in series:
                    write_api.write(BUCKET, ORG, point)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

"""Script for generating fake data, for testing pourpuses."""

import argparse
import os
import random
from datetime import date, datetime, timedelta

import requests
from dotenv import load_dotenv

CURRENT_YEAR = datetime.now().year
PAST_YEAR = CURRENT_YEAR - 1


def random_range(start, end):
    return random.random() * (end - start) + start


def random_temperature():
    return round(random_range(-10, 40), 2)


def random_datetime(min_year=PAST_YEAR, max_year=CURRENT_YEAR):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return random_range(start, end)


def generate_fake_data(number_readings=10):
    r_datetime = random_datetime()
    date = r_datetime.date().isoformat()
    temperature_readings = []

    json_data = {"date": date, "readings": temperature_readings}

    time_difference = timedelta(minutes=2)
    new_time = r_datetime

    for _ in range(number_readings):
        new_time += time_difference
        time = new_time.time().isoformat("seconds")
        temperature = random_temperature()

        temperature_readings.append(
            {
                "temperature": temperature,
                "time": time,
            }
        )

    return json_data


def fake_data_multiple_dates(number_dates: int, number_readings=10):
    dates: list[dict] = []
    time_difference = timedelta(minutes=2)

    for _ in range(number_dates):
        r_datetime = random_datetime()
        new_time = r_datetime
        readings = []

        date_log = {
            "date": {
                "year": r_datetime.year,
                "month": r_datetime.month,
                "day": r_datetime.day,
            },
            "readings": readings,
        }
        dates.append(date_log)

        for _ in range(number_readings):
            reading = {
                "temperature": random_temperature(),
                "time": {
                    "hour": new_time.hour,
                    "minutes": new_time.minute,
                    "seconds": new_time.second,
                },
            }
            new_time += time_difference
            readings.append(reading)

    return dates


def main():
    load_dotenv()
    API_TOKEN = os.environ["API_TOKEN"]
    ENDPOINT = os.environ["ENDPOINT"]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--single",
        help="Old style format for a single date.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "cuantity",
        help="Number of fake dates to create (default is 5).",
        nargs="?",
        default=5,
        type=int,
    )
    args = parser.parse_args()

    if not args.single:
        data = fake_data_multiple_dates(args.cuantity)
    else:
        data = generate_fake_data(args.cuantity)
        created_date = date.fromisoformat(data["date"])
        print(f"{created_date:%b %d %Y}")

    response = requests.post(
        url=ENDPOINT,
        json=data,
        headers={"Authorization": f"Token {API_TOKEN}"},
    )
    print(response.json())


if __name__ == "__main__":
    main()

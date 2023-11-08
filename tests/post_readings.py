import os
import random
from datetime import datetime, timedelta
from pprint import pprint

import requests
from dotenv import load_dotenv

CURRENT_YEAR = datetime.now().year
PAST_YEAR = CURRENT_YEAR - 1


def random_datetime(min_year=PAST_YEAR, max_year=CURRENT_YEAR):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


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
        temperature = round(random.random() * 30, 2)

        temperature_readings.append(
            {
                "temperature": temperature,
                "time": time,
            }
        )

    return json_data


def main():
    load_dotenv()

    API_TOKEN = os.environ["API_TOKEN"]
    ENDPOINT = os.environ["ENDPOINT"]

    data = generate_fake_data()
    response = requests.post(
        url=ENDPOINT,
        json=data,
        headers={"Authorization": f"Token {API_TOKEN}"},
    )
    pprint(response.json())


if __name__ == "__main__":
    main()

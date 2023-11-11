# Api Documentation

## Uploading Data

The data is uploaded making a `POST` request to an endpoint in the server. The
exact route is `https://domain_name/api/temperature`. Alongside the data,
an API Token should be send in the header of the request.

The following example demostrates the expected format of the data in JSON:

```json
[
    {
        "date": {
            "year": 2023,
            "month": 11,
            "day": 8
        },
        "readings": [
            {
                "temperature": 26.54,
                "time": {
                    "hour": 14,
                    "minutes": 32,
                    "seconds": 23
                }
            },
            {
                "temperature": 27.54,
                "time": {
                    "hour": 14,
                    "minutes": 34,
                    "seconds": 16
                }
            }
        ]
    },
    {
        "date": {
            "year": 2023,
            "month": 11,
            "day": 9
        },
        "readings": [
            {
                "temperature": 19.72,
                "time": {
                    "hour": 9,
                    "minutes": 15,
                    "seconds": 54
                }
            },
        ]
    }
]
```

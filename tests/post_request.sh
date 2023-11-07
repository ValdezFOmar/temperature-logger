API_TOKEN="a14607311f9e41ebdd58141189375d5ecab727ea"
ENDPOINT="http://127.0.0.1:8000/api/temperature"

curl "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $API_TOKEN" \
    -d '{
    "date": "2023-11-01",
    "readings": [
        {
            "time": "02:30:00",
            "temperature": 23.64
        },
        {
            "time": "03:30:00",
            "temperature": 24.64
        },
        {
            "time": "04:30:00",
            "temperature": 25.64
        },
        {
            "time": "05:30:00",
            "temperature": 26.64
        }
    ]
}
'

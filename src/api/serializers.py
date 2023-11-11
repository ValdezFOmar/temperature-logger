import datetime

from rest_framework import serializers

from temperature_logger.models import DateLog, TemperatureReading


class TemperatureReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = ["temperature", "time"]


class DateLogSerializer(serializers.ModelSerializer):
    readings = TemperatureReadingSerializer(many=True)

    class Meta:
        model = DateLog
        fields = ["date", "readings"]

    def create(self, validated_data):
        readings_data = validated_data.pop("readings")
        date_log, _ = DateLog.objects.get_or_create(**validated_data)

        for reading in readings_data:
            TemperatureReading.objects.create(date=date_log, **reading)

        return date_log


# New data format serializer
class DateFieldsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField()

    def validate(self, data):
        """Check that it's a valide date."""
        try:
            datetime.date(**data)
        except ValueError:
            raise serializers.ValidationError("It must be a valid date")
        return data


class TimeFieldsSerializer(serializers.Serializer):
    hour = serializers.IntegerField()
    minutes = serializers.IntegerField()
    seconds = serializers.IntegerField()

    def validate(self, data):
        """Check that is a valid time"""
        try:
            datetime.time(
                hour=data["hour"],
                minute=data["minutes"],
                second=data["seconds"],
            )
        except ValueError:
            raise serializers.ValidationError("It must be a valid time.")
        return data


class TemperatureSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    time = TimeFieldsSerializer()


class DateReadingsSerializer(serializers.Serializer):
    """Serializer for the API, allowing multiple dates to be send in the same request."""

    date = DateFieldsSerializer()
    readings = TemperatureSerializer(many=True)

    def create(self, validated_data: dict):
        readings_data = validated_data.pop("readings")
        date = datetime.date(**validated_data["date"])
        date_log, _ = DateLog.objects.get_or_create(date=date)

        for reading_data in readings_data:
            temperature = reading_data["temperature"]
            time_data = reading_data["time"]

            time = datetime.time(
                hour=time_data["hour"],
                minute=time_data["minutes"],
                second=time_data["seconds"],
            )

            TemperatureReading.objects.create(
                temperature=temperature, time=time, date=date_log
            )

        return date_log

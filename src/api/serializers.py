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

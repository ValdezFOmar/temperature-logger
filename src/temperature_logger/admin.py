from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import DateLog, TemperatureReading, User


class DateLogAdmin(admin.ModelAdmin):
    list_display = ("id", "date")


class TemperatureReadingAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "time", "temperature")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(DateLog, DateLogAdmin)
admin.site.register(TemperatureReading, TemperatureReadingAdmin)

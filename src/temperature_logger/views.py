from datetime import date

from django.shortcuts import render

from .models import DateLog, TemperatureReading


def homepage(request):
    most_recent_date = DateLog.objects.order_by("-date").first()

    if most_recent_date is None:
        most_recent_date = DateLog.objects.create(date=date.today())

    date_iso = most_recent_date.date.isoformat()
    context = {
        "date": date_iso,
    }
    return render(request, "home.html", context)


def temperatures_chart(request, date):
    selected_date = DateLog.objects.get(date=date)
    date_logs = DateLog.objects.order_by("-date")  # .exclude(date=date)
    readings = TemperatureReading.objects.filter(date=selected_date.id).order_by("time")  # type: ignore

    context = {
        "selected_date": selected_date,
        "date_logs": date_logs,
        "readings": readings,
    }
    return render(request, "temperatures.html", context)

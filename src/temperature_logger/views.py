from django.shortcuts import render

from .models import DateLog, TemperatureReading


def homepage(request):
    most_recent_date = DateLog.objects.order_by("-date")[0]
    date = most_recent_date.date.isoformat()
    context = {
        "date": date,
    }
    return render(request, "home.html", context)


def temperatures_chart(request, date):
    date_log = DateLog.objects.get(date=date)
    dates = DateLog.objects.exclude(date=date).order_by("-date")
    readings = TemperatureReading.objects.filter(date=date_log.id).order_by("time")  # type: ignore

    context = {
        "selected_date": date_log,
        "date_logs": dates,
        "readings": readings,
    }
    return render(request, "temperatures.html", context)

from django.urls import path

from . import views

urlpatterns = [
    path("temperature", views.multiple_dates_temperature, name="temperature readings"),
]

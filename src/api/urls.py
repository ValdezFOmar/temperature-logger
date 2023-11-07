from django.urls import path

from . import views

urlpatterns = [
    path("temperature", views.temperature_readings, name="temperature readings"),
]

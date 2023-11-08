from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("temperatures/<date>/", views.temperatures_chart, name="temperatures"),
]

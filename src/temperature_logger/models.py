from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    pass


# Automatically create a Token for a new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_api_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class DateLog(models.Model):
    date = models.DateField(unique=True)


class TemperatureReading(models.Model):
    temperature = models.FloatField()
    time = models.TimeField()
    date = models.ForeignKey(DateLog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["time", "date"]

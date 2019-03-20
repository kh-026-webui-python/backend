from django.db import models

# Create your models here.


class HealthCheck(models.Model):
    pong = models.BooleanField()
    database = models.BooleanField()

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class Document(models.Model):
    path = models.FilePathField(path=settings.BASE_DIR, max_length=150, unique=True)

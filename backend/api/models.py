"""
    docstring for models
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from utils.model_fields import ChoiceArrayField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class Document(models.Model):
    """
    Fields:
        path - path where file has been saved
    """
    path = models.FilePathField(path=settings.BASE_DIR, max_length=150, unique=True)


FILTER_ACTIVE = u'1'
FILTER_PLANNED = u'2'
FILTER_FREE = u'3'
FILTER_PAID = u'4'
FILTER_CHOICES = (
    (FILTER_ACTIVE, u'Active'),
    (FILTER_PLANNED, u'Planned'),
    (FILTER_FREE, u'Free'),
    (FILTER_PAID, u'Paid'),
)


class Course(models.Model):
    name = models.CharField(max_length=140)

    filters = ChoiceArrayField(
        models.CharField(choices=FILTER_CHOICES, max_length=2, blank=True, default=FILTER_PLANNED),
    )

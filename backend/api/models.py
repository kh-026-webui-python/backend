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


class Course(models.Model):
    """
    Constant:
        FILTER_CHOICES - choice for filters field
    Fields:
        name - name of course
        filters - filters, that help search course
        description - text, that describing a course
    """
    name = models.CharField(max_length=140)

    FILTER_CHOICES = (
        ('0', 'Free:Finance'),
        ('1', 'Paid:Finance'),
        ('2', 'Active:Status'),
        ('3', 'Planned:Status')
    )

    filters = ChoiceArrayField(
        models.CharField(choices=FILTER_CHOICES, max_length=2, blank=True),
    )

    description = models.TextField(default="")

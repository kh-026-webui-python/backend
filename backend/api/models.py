"""
    docstring for models
"""
from django.conf import settings, LazySettings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from utils.model_fields import ChoiceArrayField


class Profile(models.Model):
    """
    Constant:
        ENGLISH_LEVEL_CHOICES - choices for english level field
        LOCATION_CHOICES- choices for location field field
    Fields:
        user -
        birth_date - user's date of birth
        location - user's location
        english_level - user's the level of English experience
        phone_regex - show allowed number if characters for the phone number
        phone_number - user's phone number
    """

    ENGLISH_LEVEL_CHOICES = (
        ('', 'Please select one'),
        ('BG', 'beginner'),
        ('EL', 'elementary'),
        ('PI', 'pre-intermediate'),
        ('IN', 'intermediate'),
        ('UI', 'upper-intermediate'),
        ('AD', 'advanced'),
        ('PR', 'proficiency'),
    )

    LOCATION_CHOICES = (
        ('', 'Please select one'),
        ('CK', 'Cherkasy'),
        ('CH', 'Chernihiv'),
        ('CV', 'Chernivtsi'),
        ('DP', 'Dnipropetrovsk'),
        ('DT', 'Donetsk'),
        ('IF', 'Ivano-Frankivsk'),
        ('KR', 'Kharkiv'),
        ('KS', 'Kherson'),
        ('KM', 'Khmelnytskyi'),
        ('KV', 'Kiev'),
        ('KH', 'Kirovohrad'),
        ('LH', 'Luhansk'),
        ('LV', 'Lviv'),
        ('MY', 'Mykolaiv'),
        ('OD', 'Odessa'),
        ('PL', 'Poltava'),
        ('RV', 'Rivne'),
        ('SM', 'Sumy'),
        ('TP', 'Ternopil'),
        ('VI', 'Vinnytsia'),
        ('VO', 'Volyn'),
        ('ZK', 'Zakarpattia'),
        ('ZP', 'Zaporizhia'),
        ('ZT', 'Zhytomyr'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=50, default=LOCATION_CHOICES[0][1])
    english_level = models.CharField(choices=ENGLISH_LEVEL_CHOICES, max_length=50, default=ENGLISH_LEVEL_CHOICES[0][1])
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{11,13}',
                                 message="Phone number must be entered in the format: '+999999999999'. Up to 13 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=True)  # validators should be a list


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

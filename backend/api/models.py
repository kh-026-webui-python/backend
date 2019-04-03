from django.db import models
from django.conf import settings

# Create your models here.


class Document(models.Model):
    path = models.FilePathField(path=settings.BASE_DIR, max_length=150, unique=True)

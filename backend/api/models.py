from django.db import models


# Create your models here.

class Document(models.Model):
    cv = models.FileField(upload_to='CVs/')

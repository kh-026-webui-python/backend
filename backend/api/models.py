from django.db import models


class Documets(models.Model):

    descriptions=models.CharField(max_length=255, blank=True)
    document=models.FileField(upload_to='/')

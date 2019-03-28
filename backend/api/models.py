from django.db import models


class FileUpload(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey('auth.User', related_name='uploaded_file')
    size = models.IntegerField(default=0)

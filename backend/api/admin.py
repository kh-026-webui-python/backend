from api.models import Profile
from django.contrib import admin

from .models import Document

admin.site.register(Profile)
admin.site.register(Document)

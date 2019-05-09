""""
    docstring for admin
"""
from django.contrib import admin
from .models import Profile, Document, Course

from django.contrib import admin

admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(Course)

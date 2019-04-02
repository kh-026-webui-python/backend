from django.contrib import admin
from django.contrib.auth.models import User
from .models import HealthCheck

admin.site.register(HealthCheck)
#admin.site.register(User)
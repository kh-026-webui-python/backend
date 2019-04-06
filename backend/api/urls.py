""""
    docstring for api.urls
"""
from django.urls import path

from .views import HealthCheckView, UploadResumeView

urlpatterns = [
    path('health_check/', HealthCheckView.as_view()),
    path('upload_resume/', UploadResumeView.as_view())
]

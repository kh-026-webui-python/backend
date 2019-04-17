""""
    docstring for api.urls
"""
from django.urls import path

from .views import HealthCheckView, UploadResumeView

urlpatterns = [
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('upload_resume/', UploadResumeView.as_view(), name='upload_resume')
]

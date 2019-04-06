from django.urls import re_path

from .views import HealthCheckView, FileUploadView

app_name = 'health_check'

urlpatterns = [
    re_path(r'health_check/', HealthCheckView.as_view()),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]

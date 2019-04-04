from django.urls import path

from .views import HealthCheckView, UploadFileView

app_name = 'health_check'

urlpatterns = [
    path('health_check/', HealthCheckView.as_view()),
    path('upload_resume/', UploadFileView.as_view())
]

from django.urls import path

from .views import HealthCheckView
from .views import FileUploadView

app_name = 'health_check'

urlpatterns = [
    path('health_check/', HealthCheckView.as_view()),
    path('resume/', FileUploadView.as_view()),
]

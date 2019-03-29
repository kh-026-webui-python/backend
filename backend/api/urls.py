from django.urls import path

from .views import HealthCheckView

app_name = 'health_check'

urlpatterns = [
    path('health_check/', HealthCheckView.as_view()),
    path('resume/', )
]
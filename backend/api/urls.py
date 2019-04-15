from django.urls import path, re_path, include

from .views import HealthCheckView, FileUploadView, UploadResumeView

app_name = 'health_check'

urlpatterns = [
    path('health_check/', HealthCheckView.as_view()),
    path('upload_resume/', UploadResumeView.as_view()),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]

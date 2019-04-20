""""
    docstring for api.urls
"""

from django.urls import path, re_path, include

from .views import HealthCheckView, FileUploadView, UploadResumeView

urlpatterns = [
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('upload_resume/', UploadResumeView.as_view(), name='upload_resume'),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]

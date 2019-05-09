""""
    docstring for api.urls
"""

from django.urls import path, re_path, include

from .views import HealthCheckView, FileUploadView, UploadResumeView, CoursesView

urlpatterns = [
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('upload_resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('courses/', CoursesView.as_view(), name='courses'),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]

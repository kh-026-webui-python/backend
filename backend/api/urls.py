""""
    docstring for api.urls
"""

from django.urls import path, re_path, include

from .views import HealthCheckView, FileUploadView, UploadResumeView, CoursesView, CurrentProfile

urlpatterns = [
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('upload_resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('profile/', CurrentProfile.as_view(), name='current_profile'),
    path('courses/', CoursesView.as_view(), name='courses'),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]

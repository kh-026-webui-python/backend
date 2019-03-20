from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from api import views
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
# from .views import HealthCheckView
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
schema_view = get_schema_view(title='USERS API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    # re_path(r'^', schema_view, name="docs"),
    # re_path(r'^users/', include(router.urls), name="docs"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
    # path('api/health_check/', HealthCheckView.as_view()),
]
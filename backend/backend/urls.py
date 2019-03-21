from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from api import views
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
schema_view = get_schema_view(title='USERS API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    re_path(r'^login/', auth_views.auth_login),
    re_path(r'^', schema_view, name="docs"),
    re_path(r'^users/', include(router.urls), name="docs"),
]
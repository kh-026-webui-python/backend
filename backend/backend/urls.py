from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from api import views as api_views
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.authtoken import views as authtoken_views
from django.contrib import admin


router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
schema_view = get_schema_view(title='USERS API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    re_path(r'^schema/', schema_view, name="docs"),
    re_path(r'^users/', include(router.urls), name="docs"),
    re_path(r'^login/', authtoken_views.obtain_auth_token),
    re_path(r'^admin/', admin.site.urls),
]
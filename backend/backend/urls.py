""""
    docsting for urls
"""
from api import views as api_views
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', api_views.UserViewSet)
SCHEMA_VIEW = get_schema_view(title='USERS API',
                              renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [

    re_path(r'^schema/', SCHEMA_VIEW, name="docs"),
    re_path(r'^users/', include(ROUTER.urls), name="users"),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('api.urls')),

]

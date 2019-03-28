from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.serializers import User
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all()
    serializer_class = User


class FileUploadViews(APIView):


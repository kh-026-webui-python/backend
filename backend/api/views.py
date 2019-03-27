from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

def upload_file_from_users(request):
    
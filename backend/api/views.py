from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HealthCheck


class UserViewSet(viewsets.ModelViewSet):
    """

    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"ping" : "pong"})

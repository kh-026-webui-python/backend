from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import psycopg2
import os

from .models import HealthCheck


class UserViewSet(viewsets.ModelViewSet):
    """

    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HealthCheckView(APIView):

    def get(self, request):
        db = "error"
        try:
            conn = psycopg2.connect(host=os.environ.get('DB_HOST', None),
                                    database=os.environ.get('DB_NAME', 'db.postgres'),
                                    user=os.environ.get('DB_USER', ''),
                                    password=os.environ.get('DB_PASSWORD', ''))
            db = "pong"
        except Exception as e:
            print(e)
            print("Something wrong with database.")

        return Response({"server": "pong",
                         "database": db})

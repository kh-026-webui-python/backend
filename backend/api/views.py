import os
from io import TextIOWrapper

import psycopg2
from api.serializers import UserSerializer
from api.user_manager import UserManager
from django.contrib.auth.models import User
from libs.parser import CSVParser
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.views import APIView


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


def upload_CV(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']


class FileUploadView(views.APIView):
    """
    API endpoint for CSV File upload
    """

    def post(self, request, filename, format=None):

        file = TextIOWrapper(request.FILES[filename].file, encoding=request.encoding)

        user_data = CSVParser.read_from_memory(file)

        user_serializer = UserSerializer()

        response = []

        for user in user_data:

            current_user = UserManager.to_user_data(user)
            verified_data = user_serializer.validate(current_user)

            try:
                existing_user = User.objects.get(username=verified_data['username'])
            except User.DoesNotExist:
                user_serializer.create(verified_data)
                response.append(verified_data)
            else:
                response.append({'error': str(existing_user.username) + ' already exist'})

        return Response({'received data': response})

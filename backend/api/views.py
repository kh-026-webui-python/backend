"""
    Views for api app
"""
import os
import shutil

import psycopg2
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.FileValidator import FileValidator

from .models import Document
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HealthCheckView(APIView):
    """
    Ping server and database
    """

    def get(self):
        """
        Making JSON response for endpoint's get request
        """
        try:
            psycopg2.connect(host=os.environ.get('DB_HOST', None),
                             database=os.environ.get('DB_NAME', 'db.postgres'),
                             user=os.environ.get('DB_USER', ''),
                             password=os.environ.get('DB_PASSWORD', ''))
        except psycopg2.OperationalError as error:
            print(error)
            database = "error"
        else:
            database = "pong"
        return JsonResponse({"server": "pong", "database": database}, status=status.HTTP_200_OK)


class UploadResumeView(APIView):
    """
    Validate and save file on server
    """

    validator = FileValidator(
        allowed_extensions=['pdf'],
        allowed_mimetypes=['application/pdf'],
        min_size=307,
        max_size=3 * 1024 * 1024
    )

    def post(self, request):
        """
        Handle post request on server's endpoint
        """

        if request.data.get('file'):
            uploaded_file = request.data.get('file')
            try:
                self.validator(uploaded_file)
            except ValidationError as error:
                print(error)
                return JsonResponse({'error': error.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': "there is no file"}, status=status.HTTP_400_BAD_REQUEST)

        folder = 'CVs/'
        filename = uploaded_file.name
        storage = FileSystemStorage(location=folder)

        temp_cv = Document()
        temp_cv.path = f"{storage.location}/{filename}"
        try:
            temp_cv.save()
            storage.save(filename, uploaded_file)
        except IntegrityError as error:
            print(error.args[0])
            message = {'error': 'file with same name already exists'}
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        Document.objects.all().delete()
        path = FileSystemStorage("CVs/")
        shutil.rmtree(f"{path.location}")

        return Response(status=status.HTTP_200_OK)

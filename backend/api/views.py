"""
    Views for api app
"""
import logging
import os
import shutil
from io import TextIOWrapper

import psycopg2
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rollbar import logger
from utils.FileValidator import FileValidator

from utils.parser import CSVParser
from utils.user_manager import UserManager
from .models import Document, Profile
from .serializers import UserSerializer, ProfileSerializer

LOGGER = logging.getLogger('django')


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

    def get(self, request):
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


class FileUploadView(APIView):
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
            responce_data = verified_data.copy()
            try:
                existing_user = User.objects.get(username=verified_data['username'])
            except User.DoesNotExist:
                user_serializer.create(verified_data)
            else:
                responce_data['error'] = str(existing_user.username) + ' already exist'
            response.append(responce_data)

        return Response(response)


class CurrentProfile(APIView):
    """
    API endpoint for information about the authenticated user
    """

    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        """
        Updates user's data.
        :param request: HTTP request
        :return: Response(data, status)
        """
        user = User.objects.get(id=request.user.id)

        profile = Profile.objects.get(user_id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            LOGGER.error(f'Something wrong with serializer {serializer.errors}')
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        LOGGER.info(f'Profile of the {user.username} updated')

        return JsonResponse(serializer.data, status.HTTP_200_OK)

    def get(self, request):
        """
        Return user's data.
        :param request: HTTP request
        :return: Response(data, status)
        """
        user = User.objects.get(id=request.user.id)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
            LOGGER.info(f'Created profile for user: {profile.user.username}')

        serializer = UserSerializer(user, context={'request': request})

        response_data = serializer.data
        response_data['profile'] = ProfileSerializer(profile).data

        list_location = [location[1] for location in Profile.LOCATION_CHOICES]
        response_data['profile']['choices_location'] = list_location

        list_english = [level[1] for level in Profile.ENGLISH_LEVEL_CHOICES]
        response_data['profile']['choices_english'] = list_english

        return JsonResponse(response_data, status=status.HTTP_200_OK)

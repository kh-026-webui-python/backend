import os
from io import TextIOWrapper

import psycopg2
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.FileValidator import FileValidator

from utils.parser import CSVParser
from utils.user_manager import UserManager
from .models import Document
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':

        filename = request.FILES['file'].name

        if filename.endswith('.csv'):

            '''
            TODO: add file saving here
            '''

            return JsonResponse({'message': 'Sent'}, status=status.HTTP_200_OK)

        else:

            return JsonResponse({'message': 'Wrong extension, please use .csv files in your request'},
                                status=status.HTTP_409_CONFLICT)
    else:

        return JsonResponse({'message': 'Wrong method,use POST'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


class UploadResumeView(APIView):

    def post(self, request):

        validator = FileValidator(
            allowed_extensions=['pdf'],
            allowed_mimetypes=['application/pdf'],
            max_size=3 * 1024 * 1024
        )

        if request.data.get('file'):
            uploaded_file = request.data.get('file')
            try:
                validator(uploaded_file)
            except ValidationError as e:
                print(e)
                return JsonResponse({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': "there is no file"}, status=status.HTTP_400_BAD_REQUEST)

        folder = 'CVs/'
        filename = uploaded_file.name
        storage = FileSystemStorage(location=folder)

        cv = Document()
        cv.path = f"{storage.location}/{filename}"
        try:
            cv.save()
            storage.save(filename, uploaded_file)
        except IntegrityError as e:
            print(e.args[0])
            return JsonResponse({'error': 'file with same name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


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

"""
    Views for api app
"""
import os
import psycopg2

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.FileValidator import FileValidator

from .serializers import UserSerializer

from .models import Document


class UserViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@csrf_exempt
def upload_file(request):
    """
     TODO: write function docs
    """
    if request.method == 'POST':

        filename = request.FILES['file'].name

        if filename.endswith('.csv'):

            '''
            TODO: add file saving here
            '''

            return JsonResponse({'message': 'Sent'}, status=status.HTTP_200_OK)

        else:
            message = {'message': 'Wrong extension, use .csv files in your request'}
            return JsonResponse(message, status=status.HTTP_409_CONFLICT)
    else:
        message = {'message': 'Wrong method, use POST'}
        return JsonResponse(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class HealthCheckView(APIView):
    """
    Ping server and database
    """

    def get(self, request):
        """
        Making JSON response for endpoint's get request
        """
        database = "error"
        try:
            psycopg2.connect(host=os.environ.get('D_HOST', None),
                             database=os.environ.get('DB_NAME', 'db.postgres'),
                             user=os.environ.get('DB_USER', ''),
                             password=os.environ.get('DB_PASSWORD', ''))
            database = "pong"
        except psycopg2.OperationalError as error:
            print(error)

        return JsonResponse({"server": "pong", "database": database}, status=status.HTTP_200_OK)


class UploadResumeView(APIView):
    """
    Validate and save file on server
    """

    def post(self, request):
        """
        Handle post request on server's endpoint
        """
        validator = FileValidator(
            allowed_extensions=['pdf'],
            allowed_mimetypes=['application/pdf'],
            max_size=3 * 1024 * 1024
        )

        if request.data.get('file'):
            uploaded_file = request.data.get('file')
            try:
                validator(uploaded_file)
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

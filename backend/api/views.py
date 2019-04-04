from rest_framework import status
from django.contrib.auth.models import User
from .models import Document
from rest_framework import viewsets
from django.http import HttpResponse
from .serializers import UserSerializer, DocumentSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .serializers import UserSerializer
from utils.FileValidator import FileValidator

import psycopg2
import os
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    queryset = User.objects.all()
    serializer_class = User


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


#         folder = 'CVs/'
#         filename = uploaded_file.name
#         storage = FileSystemStorage(location=folder)
#
#         cv = Document()
#         cv.path = f"{storage.location}/{filename}"
#         try:
#             cv.save()
#             storage.save(filename, uploaded_file)
#         except IntegrityError as e:
#             print(e.args[0])
#             content = {'error' : 'file with same name already exists'}
#             return HttpResponse(json.dumps(content), content_type='application/json')
#
#         return Response(status=status.HTTP_201_CREATED)
class UploadResumeView(APIView):

    def post(self, request):

        validator = FileValidator(
            allowed_extensions=['pdf'],
            allowed_mimetypes=['application/pdf'],
            max_size= 3 * 1024 * 1024
        )
        # parser_class = (FileUploadParser,)
        # serializer_class = DocumentSerializer
        if request.data.get('file'):
            uploaded_file = request.data.get('file')
            try:
                validator(uploaded_file)
            except ValidationError as e:
                print(e)
                return JsonResponse({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error' : "file must have 'file' key"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

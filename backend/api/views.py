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
from rest_framework.views import APIView
import psycopg2
import os
import json


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


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = DocumentSerializer

    def post(self, request):
        # frontend check if file valid
        try:
            uploaded_file = request.data['file']
            if uploaded_file.content_type != 'application/pdf':
                raise ValueError("wrong file type")
        except KeyError as e:
            print("There is no " + e.args[0] + " in request")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            print(e)
            content = {'error' : e}
            return HttpResponse(json.dumps(content), content_type='application/json')

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
            content = {'error' : 'file with same name already exists'}
            return HttpResponse(json.dumps(content), content_type='application/json')

        return Response(status=status.HTTP_201_CREATED)

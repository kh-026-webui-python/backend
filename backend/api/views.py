from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Document
from .serializers import UserSerializer, DocumentSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
import psycopg2
import os


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

    def post(self, request):
        # frontend check if file valid
        f = request.data['file']
        # with open('pdf.pdf', 'wb') as file:
        #     file.write(f.file)
        filename = "pdf.pdf"
        fs = FileSystemStorage()
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, f)



        return Response(status=status.HTTP_201_CREATED)

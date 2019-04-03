from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from api.serializers import UserSerializer

import psycopg2
import os


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


# def upload_CV(request):
#    if request.method == 'POST' and request.FILES['file']:
#       myfile = request.FILES['file']

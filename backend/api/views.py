from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all()
    serializer_class = User


def upload_file(request):
    if (request.method == 'POST'):

        file = request.FILES[0]
        expansion = file.endwith('.csv')

        if expansion != '.csv':
            '''
            TODO: redirect on login page
            '''
            return JsonResponse({'message': 'Wrong extension, please use .csv files in your request'}, 409)

        else:
            '''
              TODO: add file saving here
              '''
            return Response(status=status.HTTP_200_OK)

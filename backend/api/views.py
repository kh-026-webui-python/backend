from django.contrib.auth.models import User
from rest_framework import viewsets, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.serializers import UserSerializer
from rest_framework.parsers import MultiPartParser

from libs.parser import CSVParser
from api.user_manager import UserManager

from io import TextIOWrapper




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FileUploadView(views.APIView):

    """
    API endpoint for CSV File upload
    """

    def post(self, request, format=None):

        file = TextIOWrapper(request.FILES['csvfile'].file, encoding=request.encoding)

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
                response.append({'error': str(existing_user.username) + 'already exist'})

        return Response({'received data': response})

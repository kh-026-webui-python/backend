from io import TextIOWrapper

from api.serializers import UserSerializer
from api.user_manager import UserManager
from django.contrib.auth.models import User
from libs.parser import CSVParser
from rest_framework import viewsets, views
from rest_framework.response import Response


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

    def post(self, request, filename, format=None):

        file = TextIOWrapper(request.FILES[filename].file, encoding=request.encoding)

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
                response.append({'error': str(existing_user.username) + ' already exist'})

        return Response({'received data': response})

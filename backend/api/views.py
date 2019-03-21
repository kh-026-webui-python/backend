from django.contrib.auth.models import User
from pytz import unicode
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from backend.backend.api.serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView


class UserLogin(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        user = serializer.validated_data['user']
        user_token, _ = Token.objects.get_or_create(user=user)
        if not token_is_active(user_token):
            user_token.delete()
            user_token = Token.objects.create(user=user)

        return Response({
            'token': user_token.key,
            'user_id': user_id,
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

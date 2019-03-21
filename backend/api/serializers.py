from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user credentials
    """
    user_name = serializers.CharField()
    user_password = serializers.CharField()

    def validate(self, attrs):
        user_name = attrs.get('user_name', '')
        user_password = attrs.get('user_password', '')

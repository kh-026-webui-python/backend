"""
    docstring for api.serializers
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Document


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        """
        Settings for serializer
        """
        model = User
        fields = ('url', 'username', 'email', 'groups')


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document model
    """
    class Meta:
        """
        Settings for serializer
        """
        model = Document
        fields = ('path',)

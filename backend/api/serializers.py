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
        model = User
        fields = ('url', 'username', 'email', 'groups')


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document model
    """
    class Meta:
        model = Document
        fields = ('path',)

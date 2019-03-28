import os

from django.contrib.auth.models import User
from rest_framework import serializers

from backend.backend.api.models import FileUpload


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class FileUploadSerializer(serializers.ModelSerializer):

    file=serializers.FileField()
    name=serializers.CharField(max_length=200)
    upload_date=serializers.DateTimeField()
    owner=serializers.IntegerField()
    size=serializers.IntegerField(default=0)

      """
        create data in BD
        """

    def create(self, validated_data):
        return FileUpload.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.file=validated_data.get('file', instance.file)
        instance.name=validated_data.get('name', instance.name)
        instance.upload_date=validated_data.get('upload_date', instance.upload_date)
        instance.owner=validated_data.get('owner', instance.owner)
        instance.size=validated_data.get('size', instance.size)
        return instance





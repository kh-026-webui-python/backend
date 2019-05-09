"""
    docstring for api.serializers
"""

from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Document, Profile, Course


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('location', 'birth_date')

    def validate(self, data):
        if 'birth_date' in data:
            data['birth_date'] = datetime.strptime(data['birth_date'], "%d.%m.%y").strftime('%Y-%m-%d')
        return {key: value for key, value in data.items() if key in self.fields}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model
    """
    profile = ProfileSerializer(required=True)

    class Meta:
        """
        Settings for serializer
        """
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        Profile.objects.create(user=user, **profile_data)

        return user


    def validate(self, data):
        if 'profile' in data:
            data['profile'] = ProfileSerializer().validate(data['profile'])

        return {key: value for key, value in data.items() if key in self.fields}


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


class ChoiceArrayField(serializers.Field):
    """
    Serializer for filters field in Course model
    """
    def to_representation(self, value):
        """
        :param value: list of filters in non human readable formate
        :return: filters: string that represent list of filters
        """
        filters = "[ "
        for filter in value:
            filters += '\"' + Course.FILTER_CHOICES[int(filter)][1] + "\", "
        return filters[:-2] + " ]"


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    filters = ChoiceArrayField()

    class Meta:
        model = Course
        fields = ('name', 'filters', 'description')
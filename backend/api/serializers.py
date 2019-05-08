"""
    docstring for api.serializers
"""

from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Document
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for Profile model
    """

    location = serializers.CharField(source='get_location_display')
    english_level = serializers.CharField(source='get_english_level_display')

    class Meta:
        model = Profile
        fields = ('location', 'birth_date', 'english_level', 'phone_number', 'english_level')

    def validate(self, data):
        if 'birth_date' in data:
            data['birth_date'] = datetime.strptime(data['birth_date'], "%d.%m.%y").strftime('%Y-%m-%d')
        return {key: value for key, value in data.items() if key in self.fields}

    def get_location(self, obj):
        return obj.get_location_display()

    def get_english_level(self, obj):
        return obj.get_english_level_display()


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
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'date_joined', 'profile')
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

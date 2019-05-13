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

    def update(self, instance, validated_data):
        print('asd')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        # instance.user.first_name = user.get('first_name')
        print('hey')
        return instance

    #
    # def validate(self, data):
    #     if 'birth_date' in data:
    #         data['birth_date'] = datetime.strptime(data['birth_date'], "%d.%m.%y").strftime('%Y-%m-%d')
    #     return {key: value for key, value in data.items() if key in self.fields}

    def get_location(self, obj):
        return obj.get_location_display()

    def get_english_level(self, obj):
        return obj.get_english_level_display()


class UserSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        nested_data = self.initial_data
        nested_profile = instance.profile
        # nested_data = validated_data.pop('profile')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)

        # instance.user.first_name = user.get('first_name')
        # return instance

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

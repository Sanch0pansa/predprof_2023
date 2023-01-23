from rest_framework import serializers
from API.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


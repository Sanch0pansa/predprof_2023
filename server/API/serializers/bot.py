from rest_framework import serializers
from API.models import User


class TelegramMessagesPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmailMessagesPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
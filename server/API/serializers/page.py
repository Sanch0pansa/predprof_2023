from rest_framework import serializers
from API.models import Page


class PageCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PageRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

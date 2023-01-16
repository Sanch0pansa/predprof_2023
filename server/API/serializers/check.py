from rest_framework import serializers
from API.models import Check


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'

    def getBadChecks(self, obj):
        return obj.response_status_code

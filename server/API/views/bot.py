from rest_framework import generics
from rest_framework import serializers
from django.http import JsonResponse
from API.models import Check
import json
class get_messages(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if request.POST['_token'] == '123456':
            checks = Check.objects.exclude(response_status_code='200')
            return JsonResponse(checks, safe=False)
        else:
            return JsonResponse('Не верный токен')
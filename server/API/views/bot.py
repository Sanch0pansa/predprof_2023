from rest_framework import generics
from rest_framework import serializers
from django.http import JsonResponse
from API.models import Check
import json

class get_messages(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        checks = Check.objects.all().order_by('page_id', '-checked_at').distinct('page_id')
        return JsonResponse(list(checks.values()), safe=False)
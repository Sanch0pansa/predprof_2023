from rest_framework import generics
from django.http import JsonResponse

import json
class get_telegram_messages(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if request.POST['_token'] == '123456':
            return JsonResponse({'foo':'bar'})
        else:
            return HttpResponse(json.dumps(['Не верный токен']), content_type='application/json')
from rest_framework import generics
from API.models import Check, Page
from API.serializers.check import CheckSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import requests
from API.funcs import getData

config = [i.split() for i in open('tokens.txt').readlines()][1]
bot_token = [i.split() for i in open('tokens.txt').readlines()][0]

class GetPagesForCheck(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            sites = {}
            if data['_token'] == config[1]:
                pages = list((Page.objects.filter(is_checking=True)).values('id', 'url'))
                for i in pages:
                    sites[i['id']] = i['url']
                return JsonResponse(sites)
            else:
                return JsonResponse({'detail': 'Неправильный токен'})
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'})


class CheckCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data['_token'] == config[1]:
                pages = data['data']
                for i in pages:
                    page_id = i
                    res_code = pages[i][0]
                    res_time = pages[i][1]
                    checked_at = pages[i][2]
                    if res_code != 200:
                        last_check_result = 0
                    elif res_time < 1000:
                        last_check_result = 2
                    elif res_time >= 1000:
                        last_check_result = 1
                    check = Check(page_id=page_id,
                                  response_status_code=res_code,
                                  response_time=res_time,
                                  check_status=last_check_result,
                                  checked_at=checked_at)
                    check.save()
                requests.post('http://127.0.0.1:1000/check_messages', json={'_token': bot_token[1]})
                return JsonResponse({'success': True})
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()

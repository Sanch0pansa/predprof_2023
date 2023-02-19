from rest_framework import generics
from API.models import Check, Page
from API.serializers.check import CheckSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import requests
from API.funcs import getData
from project.settings import bot_host
from django.db.models import Avg

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
                return JsonResponse({'detail': 'Неправильный токен'}, status=400)
        except Exception:
            return JsonResponse({'success': False}, status=500)


class CheckCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data['_token'] == config[1]:
                pages = data['data']
                averageTime = {}
                temp = Check.objects.values('page_id').annotate(avg_time=Avg('response_time')).order_by('-page_id')
                for i in temp:
                    averageTime[str(i['page_id'])] = round(i['avg_time'])
                for i in pages:
                    page_id = i
                    res_code = str(pages[i][0])
                    res_time = pages[i][1]
                    checked_at = pages[i][2]
                    if i in averageTime:
                        time = averageTime[i]
                        if time < 100:
                            k = 2.5
                        else:
                            k = 1.5
                        if not res_code.startswith('2'):
                            last_check_result = '0'
                        elif res_time/time < k:
                            last_check_result = '2'
                        else:
                            last_check_result = '1'
                    else:
                        if not res_code.startswith('2'):
                            last_check_result = 0
                        else:
                            last_check_result = 2
                    check = Check(page_id=page_id,
                                  response_status_code=res_code,
                                  response_time=res_time,
                                  check_status=last_check_result,
                                  checked_at=checked_at)
                    check.save()
                try:
                    requests.post(f'{bot_host}/check_messages', json={'_token': bot_token[1]})
                except Exception:
                    print('Бот не запущен')
                return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()

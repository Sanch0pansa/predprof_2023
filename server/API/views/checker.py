from rest_framework import generics
from API.models import Check, Page
from API.serializers.check import CheckSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

config = [i.split() for i in open('tokens.txt').readlines()][1]


class GetPagesForCheck(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            sites = {'pages': []}
            if data['_token'] == config[1]:
                pages = list((Page.objects.filter(is_checking=True)).values())
                for i in pages:
                    sites['pages'].append(i['url'])
                return JsonResponse(sites)
            else:
                return JsonResponse({'detail': 'Wrong token'})
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'})


class CheckCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            if data['_token'] == config[1]:
                page = list((Page.objects.filter(url=data['url'])).values())[0]
                if data['response_status_code'] != '200':
                    last_check_result = 0
                elif data['response_time'] < 1000:
                    last_check_result = 2
                elif data['response_time'] >= 1000:
                    last_check_result = 1
                check = Check(page_id=page['id'],
                              response_status_code=data['response_status_code'],
                              response_time=data['response_time'],
                              check_status=last_check_result)
                check.save()
                return JsonResponse({'success': True})
        except Exception as ex:
            print(ex)
            return JsonResponse({'success': False})


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()
from rest_framework import generics
from django.http import JsonResponse
from API.models import Check, User
from django.utils import timezone
from rest_framework.permissions import AllowAny
config = [i.split() for i in open('conf.txt').readlines()][0]
class GetBotMessages(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.POST
        if data['_token'] == config[1]:
            query = (
                'SELECT 1 as id, pages.url, users.email, users.telegram_id, sub1.response_status_code, sub1.response_time\n'
                'FROM "API_page" as pages\n'
                'JOIN (SELECT DISTINCT ON (subs.id) checks.page_id, subs.user_id, checks.response_status_code, checks.response_time \n'
                '            FROM "API_subscription" as subs\n'
                '            JOIN "API_check" as checks on subs.page_id=checks.page_id\n'
                '            ORDER BY subs.id ASC, checks.page_id ASC, checked_at DESC) as sub1\n'
                '            ON pages.id=sub1.page_id\n'
                'JOIN "API_user" as users\n'
                'ON users.id=sub1.user_id\n')
            checks = (Check.objects.raw(query))
            pages = {}
            for i in checks:
                if i.url not in pages:
                    pages[i.url] = {
                        "url": i.url,
                        "response_status_code": i.response_status_code,
                        "response_time": i.response_time,
                        "subscribers_telegram": [],
                        "subscribers_email": []
                    }
                pages[i.url]['subscribers_email'].append(i.email)
                if i.telegram_id is not None:
                    pages[i.url]['subscribers_telegram'].append(i.telegram_id)

            return JsonResponse(list(pages.values()), safe=False)
        else:
            return JsonResponse({'detail': 'Wrong token'})


class VerifyUser(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.POST
        if data['_token'] == config[1]:
            try:
                checkJson = ((User.objects.filter(telegram_verification_code=data['telegram_verification_code'])).values())[
                    0]
                checkData = User.objects.get(pk=checkJson['id'])
            except Exception:
                return JsonResponse({'succes': False})
            dateNow = timezone.now()
            if checkJson['telegram_verification_code_date'] > dateNow:
                checkData.telegram_id = request.POST['telegram_id']
                checkData.telegram_verification_code = None
                checkData.telegram_verification_code_date = None
                checkData.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'detail': 'Wrong token'})

class CheckUser(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.POST
        if data['_token'] == config[1]:
            user = list((User.objects.filter(telegram_id=data['telegram_id'])).values())
            if user != []:
                return JsonResponse({'user_verified': True})
            else:
                return JsonResponse({'user_verified': False})
        else:
            return JsonResponse({'detail': 'Wrong token'})

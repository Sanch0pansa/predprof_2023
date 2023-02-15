from rest_framework import generics
from django.http import JsonResponse
from API.models import Check, User
from django.utils import timezone
from API.funcs import getData
from rest_framework.permissions import AllowAny

config = [i.split() for i in open('tokens.txt').readlines()][0]


class GetBotMessages(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = getData(request)
        if data['_token'] == config[1]:
            query = (
                'SELECT 1 as id, pages.url, users.email, users.telegram_id, sub1.response_status_code, sub1.response_time, sub1.checked_at '
                'FROM "API_page" as pages '
                'JOIN (SELECT DISTINCT ON (subs.id) checks.page_id, subs.user_id, checks.response_status_code, checks.response_time, checks.checked_at '
                '            FROM "API_subscription" as subs '
                '            JOIN "API_check" as checks on subs.page_id=checks.page_id '
                '            ORDER BY subs.id ASC, checks.id DESC, checks.page_id ASC, checked_at DESC) as sub1 '
                '            ON pages.id=sub1.page_id '
                'JOIN "API_user" as users '
                'ON users.id=sub1.user_id '
                'WHERE NOT(sub1.response_status_code=\'200\')')
            checks = (Check.objects.raw(query))
            pages = {}
            for i in checks:
                if i.url not in pages:
                    pages[i.url] = {
                        'url': i.url,
                        'response_status_code': i.response_status_code,
                        'response_time': i.response_time,
                        'checked_at': i.checked_at,
                        'subscribers_telegram': [],
                        'subscribers_email': []
                    }
                pages[i.url]['subscribers_email'].append(i.email)
                if i.telegram_id is not None:
                    pages[i.url]['subscribers_telegram'].append(i.telegram_id)

            return JsonResponse(list(pages.values()), safe=False)
        else:
            return JsonResponse({'detail': 'Неправильный токен'})


class VerifyUser(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data['_token'] == config[1]:
                try:
                    checkJson = ((User.objects.filter(telegram_verification_code=data['telegram_verification_code'])).values())[0]
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
                return JsonResponse({'detail': 'Неправильный токен'})
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class CheckUser(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data['_token'] == config[1]:
                user = list((User.objects.filter(telegram_id=data['telegram_id'])).values())
                if user != []:
                    return JsonResponse({'user_verified': True})
                else:
                    return JsonResponse({'user_verified': False})
            else:
                return JsonResponse({'detail': 'Неправильный токен'})
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)

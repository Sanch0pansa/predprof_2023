from rest_framework import generics
from django.http import JsonResponse
from API.models import Check, User
from django.utils import timezone
from API.funcs import getData
from rest_framework.permissions import AllowAny
from API.views.page import errors

config = [i.split() for i in open('tokens.txt').readlines()][0]


def get_messages():
    print("some msgs here")
    query = (
        'SELECT 1 as id, pages.url, users.email, users.telegram_id, sub1.response_status_code, sub1.checked_at '
        'FROM "API_page" as pages '
        'JOIN (SELECT DISTINCT ON (subs.id) checks.page_id, subs.user_id, checks.response_status_code, checks.check_status, checks.checked_at '
        '            FROM "API_subscription" as subs '
        '            JOIN "API_check" as checks on subs.page_id=checks.page_id '
        '            ORDER BY subs.id ASC, checks.id DESC, checks.page_id ASC, checked_at DESC) as sub1 '
        '            ON pages.id=sub1.page_id '
        'JOIN "API_user" as users '
        'ON users.id=sub1.user_id '
        'WHERE NOT(sub1.check_status=\'2\')')
    checks = (Check.objects.raw(query))
    pages = {}
    for i in checks:
        if i.url not in pages:
            try:
                error = errors[i.response_status_code]
            except Exception:
                error = {'error_description': 'Неизвестная ошибка',
                         'reasons': ['Не известны']}
            pages[i.url] = {
                'url': i.url,
                'error': error,
                'checked_at': i.checked_at.isoformat(),
                'subscribers_telegram': [],
                'subscribers_email': []
            }
        pages[i.url]['subscribers_email'].append(i.email)
        if i.telegram_id is not None:
            pages[i.url]['subscribers_telegram'].append(i.telegram_id)

    return list(pages.values())


def verify_user(telegram_id, code):
    try:
        checkJson = ((User.objects.filter(telegram_verification_code=code)).values())[0]
        checkData = User.objects.get(pk=checkJson['id'])
    except Exception:
        return JsonResponse({'succes': False})
    dateNow = timezone.now()
    if checkJson['telegram_verification_code_date'] > dateNow:
        checkData.telegram_id = telegram_id
        checkData.telegram_verification_code = None
        checkData.telegram_verification_code_date = None
        checkData.save()
        return {'success': True}
    else:
        return {'success': True}


def check_user(telegram_id):
    user = list((User.objects.filter(telegram_id=telegram_id)).values())
    return {'user_verified': user != []}

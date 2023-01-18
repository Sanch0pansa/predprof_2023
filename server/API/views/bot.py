from rest_framework import generics
from rest_framework import serializers
from django.http import JsonResponse
from API.models import Check, Subscription
from django.db.models.expressions import RawSQL
import json

class GetBotMessages(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        query = '''SELECT 1 as id, pages.url, users.login, users.telegram_id, sub1.response_status_code, sub1.response_time 
FROM "API_page" as pages
JOIN (SELECT DISTINCT ON (subs.id) checks.page_id, subs.user_id, checks.response_status_code, checks.response_time 
		FROM "API_subscription" as subs
		JOIN "API_check" as checks on subs.page_id=checks.page_id
		ORDER BY subs.id ASC, checks.page_id ASC, checked_at DESC) as sub1
ON pages.id=sub1.page_id
JOIN "API_user" as users
ON users.id=sub1.user_id
WHERE NOT (sub1.response_status_code='200')'''
        checks = (Check.objects.raw(query))
        pages = {}
        for i in checks:
            print(pages)
            if i.url not in pages:
                pages[i.url] = {
                    "url": i.url,
                    "response_status_code": i.response_status_code,
                    "response_time": i.response_time,
                    "subscribers_telegram": [],
                    "subscribers_email": []
                }
            pages[i.url]['subscribers_email'].append(i.login)
            if i.telegram_id is not None:
                pages[i.url]['subscribers_telegram'].append(i.telegram_id)
            print(pages)

        return JsonResponse(list(pages.values()), safe=False)
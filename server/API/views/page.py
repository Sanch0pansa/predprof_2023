from rest_framework import generics
from API.models import Page, Review, Check, Report, Subscription, User
from API.serializers.page import PageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from API.permissions import IsAdmin
from django.http import JsonResponse
from django.core.paginator import Paginator
from API.funcs import getData
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

errors = {'500': {'error_description': 'Ошибка сервера',
                  'reasons': [
                      'Перезагрузка сервера',
                      'Ошибка в коде сервера',
                      'Ошибка в файле .htaccess']},
          '808': {'error_description': 'Неизвестная ошибка',
                  'reasons': ['Сайт обрывает соединение']}}


class PageListView(generics.ListAPIView):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Page.objects.all()


class PageCreate(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PageSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            user = request.user
            page = list(Page.objects.filter(url=data['url']).exclude(is_moderated=False))
            if page:
                return JsonResponse({'errors': {'url': ['Сайт с такой ссылкой уже есть в базе']}})
            page = Page(name=data['name'],
                        url=data['url'],
                        description=data['description'],
                        added_by_user_id=user.id)
            try:
                page.full_clean()
            except ValidationError as ex:
                return JsonResponse({'errors': dict(ex)})
            page.save()
            return JsonResponse({'success': True})
        except Exception as ex:
            print(ex)
            return JsonResponse({'success': False}, status=400)


class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class GetPopularPages(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, *args, **kwargs):
        try:
            try:
                reviews = Review.objects.raw('SELECT pages.id, pages.name, pages.url, COUNT(revs.id) AS "total" '
                                             'FROM "API_page" AS pages '
                                             'LEFT JOIN "API_review" AS revs ON revs.page_id=pages.id '
                                             'WHERE revs.is_published = true AND pages.is_checking = true '
                                             'GROUP BY pages.id '
                                             'ORDER BY total DESC '
                                             'LIMIT 3 ')
                pageIds = [i.id for i in reviews]
                checks = Check.objects.raw('SELECT DISTINCT ON (pages.id) pages.id, checks.check_status '
                                           'FROM "API_page" AS pages '
                                           'JOIN "API_check" AS checks ON checks.page_id=pages.id '
                                           f'WHERE pages.id in ({pageIds[0]}, {pageIds[1]}, {pageIds[2]}) '
                                           'ORDER BY pages.id DESC, checks.id DESC')
            except Exception as ex:
                return JsonResponse({'detail': 'Ошибка, меньше 3 сайтов с подтверждёнными отзывами'}, status=400)
            temp = {}
            for i in checks:
                temp[i.id] = i.check_status
            res = []
            for i in reviews:
                res.append({'id': i.id,
                            'name': i.name,
                            'url': i.url,
                            'check_status': temp[i.id]})
            return JsonResponse(res, safe=False)
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class GetSiteStats(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            pages = Page.objects.only('id').count()
            reports = Report.objects.only('id').count()
            reviews = Review.objects.only('id').count()
            failures = Check.objects.only('id').exclude(response_status_code=200).count()
            result = {'total_pages': pages, 'total_reports': reports, 'total_reviews': reviews,
                      'detected_failures': failures}
            return JsonResponse(result)
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class GetCheckingPages(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            pages = Page.objects.raw('SELECT DISTINCT ON (pages.id) pages.id, pages.name, pages.url, '
                                     'checks.response_time, checks.checked_at, checks.check_status, '
                                     'ROUND(AVG(reviews.mark), 2) as rating '
                                     'FROM "API_page" AS pages '
                                     'LEFT JOIN "API_check" AS checks ON checks.page_id=pages.id '
                                     'LEFT JOIN "API_review" AS reviews ON (pages.id=reviews.page_id AND reviews.is_published=true) '
                                     'WHERE pages.is_checking = true '
                                     'GROUP BY pages.id, checks.response_time, checks.checked_at, checks.check_status '
                                     'ORDER BY pages.id DESC, checks.checked_at DESC ')
            result = []
            for i in pages:
                result.append({'id': i.id,
                               'name': i.name,
                               'url': i.url,
                               'last_check_time': i.checked_at,
                               'last_check_timeout': i.response_time,
                               'check_status': i.check_status,
                               'rating': i.rating})
            result = Paginator(result, 5)
            return JsonResponse({'num_pages': result.num_pages, 'pages': list(result.page(data['page_number']))})
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class GetAccountData(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            subs = Subscription.objects.raw(
                'SELECT DISTINCT ON (checks.page_id) pages.id, pages.name, checks.check_status '
                'FROM "API_subscription" as subs '
                'LEFT JOIN "API_check" as checks ON checks.page_id=subs.page_id '
                'JOIN "API_page" as pages ON subs.page_id=pages.id '
                f'WHERE user_id={user.id} '
                'ORDER BY checks.page_id DESC, checks.id DESC ')
            result = []
            for i in subs:
                result.append({'id': i.id,
                               'name': i.name,
                               'check_status': i.check_status})
            return JsonResponse(result, safe=False)
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class PageChecks(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, id, *args, **kwargs):
        try:
            time = timezone.now()
            checks = list(Check.objects.filter(page_id=id, checked_at__range=(time - timedelta(days=3), time))
                          .values('checked_at', 'response_time', 'check_status')
                          .order_by('id'))
            return JsonResponse(checks, safe=False)
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'})


class PageReviews(generics.GenericAPIView):
    serializer_class = PageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsAdmin()]

    def get(self, request, id, *args, **kwargs):
        try:
            checks = list(Review.objects.filter(page_id=id)
                          .select_related('added_by_user')
                          .values('id', 'added_at', 'mark', 'message', 'added_by_user__username', 'added_by_user')
                          .filter(is_published=True))
            return JsonResponse(checks, safe=False)
        except Exception as ex:
            return JsonResponse({'detail': 'Something went wrong'})

    def post(self, request, id, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            review = Review.objects.create(added_by_user_id=user.id, page_id=id, message=data['message'],
                                           mark=data['mark'])
            review.save()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=400)


class PageReports(generics.GenericAPIView):
    serializer_class = PageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsAdmin()]

    def get(self, request, id, *args, **kwargs):
        try:
            checks = list(Report.objects.filter(page_id=id)
                          .select_related('added_by_user')
                          .values('id', 'added_at', 'message', 'added_by_user__username', 'added_by_user')
                          .filter(is_published=True))
            return JsonResponse(checks, safe=False)
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'}, status=400)

    def post(self, request, id, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            report = Report.objects.create(added_by_user_id=user.id, page_id=id, message=data['message'],
                                           added_at=data['added_at'])
            report.save()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=400)


class GetPageData(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, id, *args, **kwargs):
        try:
            page = list(Page.objects.filter(id=id).values('name', 'url', 'description'))
            if page:
                page = page[0]
            return JsonResponse(page, safe=False)
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'}, status=400)


class Subscriptions(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Subscription

    def get(self, request, id, *args, **kwargs):
        try:
            user = request.user
            check_sub = list(Subscription.objects.filter(page_id=id, user_id=user.id))
            if check_sub:
                return JsonResponse({'subscribed': True})
            else:
                return JsonResponse({'subscribed': False})
        except Exception as ex:
            return JsonResponse({'detail': 'Exception'}, status=400)

    def post(self, request, id, *args, **kwargs):
        try:
            user = request.user
            check_sub = list(Subscription.objects.filter(page_id=id, user_id=user.id))
            if not check_sub:
                sub = Subscription.objects.create(page_id=id, user_id=user.id)
                sub.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        except Exception as ex:
            return JsonResponse({'detail': 'Exception'}, status=400)

    def delete(self, request, id, *args, **kwargs):
        try:
            user = request.user
            check_sub = Subscription.objects.filter(page_id=id, user_id=user.id)
            if list(check_sub):
                check_sub.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        except Exception:
            return JsonResponse({'detail': 'Exception'}, status=500)


class Events(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            result = {'working': 0,
                      'lazy_loading': 0,
                      'not_working': 0}
            subPages = Subscription.objects.filter(user_id=user.id).values('page_id')
            pageIds = [i['page_id'] for i in subPages]
            time = timezone.now()
            reports = Report.objects.filter(page_id__in=pageIds,
                                            is_published=True,
                                            added_at__range=(time - timedelta(days=3), time)) \
                .select_related('page', 'added_by_user') \
                .values('page', 'page__name', 'added_at', 'message', 'added_by_user', 'added_by_user__username')
            reviews = Review.objects.filter(page_id__in=pageIds,
                                            is_published=True,
                                            added_at__range=(time - timedelta(days=3), time)) \
                .select_related('page', 'added_by_user') \
                .values('page', 'page__name', 'added_at', 'mark', 'message', 'added_by_user', 'added_by_user__username')

            checks = Check.objects.filter(page_id__in=pageIds,
                                          checked_at__range=(time - timedelta(days=3), time)) \
                .select_related('page') \
                .exclude(check_status='2') \
                .values('page_id', 'page__name', 'check_status', 'checked_at', 'response_status_code', 'response_time',
                        'check_status') \
                .distinct('page_id') \
                .order_by('page_id', '-id')

            pages = Check.objects.filter(page_id__in=pageIds) \
                .values('check_status') \
                .distinct('page_id') \
                .order_by('page_id', '-id')
            for i in pages:
                if i['check_status'] == '2':
                    result['working'] += 1
                if i['check_status'] == '1':
                    result['lazy_loading'] += 1
                elif i['check_status'] == '0' or i['check_status'] == '3':
                    result['not_working'] += 1

            result['events'] = []

            for i in checks:
                if i['response_status_code'] == '200' and i['check_status'] == '2':
                    continue
                elif i['check_status'] == '1':
                    result['events'].append({'type': 'lazy_loading',
                                             'page': {'id': i['page_id'],
                                                      'name': i['page__name']},
                                             'detail': {'time': i['response_time'],
                                                        'reasons': [
                                                            'Большой трафик',
                                                            'DDOS',
                                                            'т.д.']},
                                             'message_datetime': i['checked_at']})
                else:
                    result['events'].append({'type': 'failure',
                                             'page': {'id': i['page_id'],
                                                      'name': i['page__name']},
                                             'detail': errors[i['response_status_code']],
                                             'message_datetime': i['checked_at']})
            for i in reports:
                result['events'].append({'type': 'report',
                                         'page': {'id': i['page'],
                                                  'name': i['page__name']},
                                         'detail': {
                                             'message': i['message'],
                                             'user': {
                                                 'id': i['added_by_user'],
                                                 'username': i['added_by_user__username']
                                             }
                                         },
                                         'message_datetime': i['added_at']
                                         })

            for i in reviews:
                result['events'].append({'type': 'review',
                                         'page': {'id': i['page'],
                                                  'name': i['page__name']},
                                         'detail': {
                                             'mark': i['mark'],
                                             'message': i['message'],
                                             'user': {
                                                 'id': i['added_by_user'],
                                                 'username': i['added_by_user__username']
                                             }
                                         },
                                         'message_datetime': i['added_at']
                                         })

            return JsonResponse(result, safe=False)

        except Exception as ex:
            print(ex)
            return JsonResponse({'success': False}, status=500)

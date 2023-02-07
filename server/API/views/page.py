from rest_framework import generics
from API.models import Page, Review, Check, Report, Subscription
from API.serializers.page import PageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from API.funcs import getData
from django.core.exceptions import ValidationError

class PageListCreateView(generics.ListCreateAPIView):
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
            return JsonResponse({'success': False}, status=400)


class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class GetPopularPages(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, *args, **kwargs):
        try:
            try:
                reviews = Review.objects.raw('SELECT pages.id, COUNT(revs.id) AS "total" '
                                             'FROM "API_page" as pages '
                                             'LEFT JOIN "API_review" as revs ON revs.page_id=pages.id '
                                             'GROUP BY pages.id '
                                             'ORDER BY total DESC '
                                             'LIMIT 3')
                pageIds = [i.id for i in reviews]
            except Exception as ex:
                return JsonResponse({'detail': 'Ошибка, меньше 3 сайтов в базе'})
            checks = list(Check.objects
                          .prefetch_related('checks')
                          .values('page_id', 'page__name', 'page__url', 'check_status')
                          .filter(Q(page_id=pageIds[0]) | Q(page_id=pageIds[1]) | Q(page_id=pageIds[2]))
                          .order_by('-page_id', '-checked_at')
                          .distinct('page_id'))[:3]
            for i in checks:
                i['id'] = i.pop('page_id')
                i['name'] = i.pop('page__name')
                i['url'] = i.pop('page__url')
                i['check_status'] = i.pop('check_status')
            return JsonResponse(checks, safe=False)
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
            pages = Check.objects \
                .select_related('page') \
                .values('page__id', 'page__name', 'page__url', 'check_status', 'response_time', 'checked_at') \
                .order_by('-page__id', '-id') \
                .distinct('page__id')
            result = []
            for i in pages:
                result.append({'id': i['page__id'],
                               'name': i['page__name'],
                               'url': i['page__url'],
                               'last_check_time': i['checked_at'],
                               'last_check_timeout': i['response_time'],
                               'check_status': i['check_status']})
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
                'JOIN "API_check" as checks ON checks.page_id=subs.page_id '
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


class GetPageChecks(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, id, *args, **kwargs):
        try:
            checks = list(Check.objects.filter(page_id=id).values('checked_at', 'response_time', 'check_status'))
            return JsonResponse(checks, safe=False)
        except Exception:
            return JsonResponse({'detail': 'Something went wrong'})


class GetPageReviews(generics.GenericAPIView):
    serializer_class = PageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get(self, request, id, *args, **kwargs):
        try:
            checks = list(Review.objects.filter(page_id=id)
                          .select_related('added_by_user')
                          .values('added_at', 'mark', 'message', 'added_by_user__username', 'added_by_user')
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


class GetPageReports(generics.GenericAPIView):
    serializer_class = PageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get(self, request, id, *args, **kwargs):
        try:
            checks = list(Report.objects.filter(page_id=id)
                          .select_related('added_by_user')
                          .values('added_at', 'message', 'added_by_user__username', 'added_by_user')
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
            return JsonResponse({'detail': "Exception"}, status=400)

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
            return JsonResponse({'detail': "Exception"}, status=400)

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
            return JsonResponse({'detail': "Exception"}, status=400)

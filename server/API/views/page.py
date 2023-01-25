from rest_framework import generics
from API.models import Page, Review, Check, Report
from API.serializers.page import PageSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

class PageListCreateView(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class GetPopularPages(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get(self, request, *args, **kwargs):
        try:
            reviews = Review.objects.raw('SELECT pages.id, COUNT(revs.id) AS "total" '
                                         'FROM "API_page" as pages '
                                         'LEFT JOIN "API_review" as revs ON revs.page_id=pages.id '
                                         'GROUP BY pages.id '
                                         'ORDER BY total DESC '
                                         'LIMIT 3')
            pageIds = [i.id for i in reviews]
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Ошибка, меньше 3 сайтов в базе'})
        checks = list(Check.objects
                      .prefetch_related('checks')
                      .values('page_id', 'page__name', 'page__url', 'response_time', 'response_status_code')
                      .filter(Q(page_id=pageIds[0]) | Q(page_id=pageIds[1]) | Q(page_id=pageIds[2]))
                      .order_by('-checked_at'))[:3]
        for i in checks:
            i['id'] = i.pop('page_id')
            i['name'] = i.pop('page__name')
            i['url'] = i.pop('page__url')
            i['last_check_result'] = i.pop('response_time')
            if i['response_status_code'] != '200':
                i['last_check_result'] = 0
            elif i['last_check_result'] < 1000:
                i['last_check_result'] = 2
            elif i['last_check_result'] >= 1000:
                i['last_check_result'] = 1
            i.pop('response_status_code')
        return JsonResponse(checks, safe=False)


class GetSiteStats(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pages = Page.objects.only('id').count()
        reports = Report.objects.only('id').count()
        reviews = Review.objects.only('id').count()
        failures = Check.objects.only('id').exclude(response_status_code=200).count()
        result = {'total_pages': pages, 'total_reports': reports, 'total_reviews': reviews, 'detected_failures': failures}
        return JsonResponse(result)


class GetCheckingPages(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            pages = Check.objects\
                .select_related('page')\
                .values('page__id', 'page__name', 'page__url', 'response_status_code', 'response_time', 'checked_at')\
                .order_by('-page__id', '-id')\
                .distinct('page__id')
            print(pages.query)
            result = []
            n = -1
            for i in pages:
                n += 1
                result.append({'id': i['page__id'],
                               'name': i['page__name'],
                               'url': i['page__url'],
                               'last_check_time': i['checked_at'],
                               'last_check_result': None,
                               'last_check_timeout': i['response_time']})
                item = result[n]
                if i['response_status_code'] != '200':
                    item['last_check_result'] = 0
                elif i['response_time'] < 1000:
                    item['last_check_result'] = 2
                elif i['response_time'] >= 1000:
                    item['last_check_result'] = 1
            result = Paginator(result, 5)
            return JsonResponse({'num_pages': result.num_pages, 'pages': list(result.page(data['page_id']))}, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Something went wrong...'})
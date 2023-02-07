from API.funcs import getData
from rest_framework import generics
from API.models import Page, Review, Report
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.http import JsonResponse


class GetModerateCategories(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            pages = Page.objects.filter(is_moderated=None).only('id').count()
            reviews = Review.objects.filter(is_moderated=None).only('id').count()
            reports = Report.objects.filter(is_moderated=None).only('id').count()
            return JsonResponse({'pages': pages,
                                 'reviews': reviews,
                                 'reports': reports})
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetModerationPages(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            pages = list(Page.objects
                         .filter(is_moderated=None)
                         .select_related('added_by_user')
                         .values('id', 'name', 'description', 'url', 'added_by_user', 'added_by_user__username'))
            pagesForModerate = []
            for i in pages:
                pagesForModerate.append({'id': i['id'],
                              'name': i['name'],
                              'description': i['description'],
                              'url': i['url'],
                              'user': {'id': i['added_by_user'],
                                       'username': i['added_by_user__username']}})
            return JsonResponse(pagesForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetModerationReviews(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            reviews = list(Review.objects
                           .filter(is_moderated=None)
                           .select_related('added_by_user', 'page')
                           .values('id', 'page__id', 'page__name', 'page__url', 'mark', 'message', 'added_at', 'added_by_user', 'added_by_user__username'))
            reviewsForModerate = []
            for i in reviews:
                reviewsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'user': {'id': i['added_by_user'],
                              'username': i['added_by_user__username']},
                      'mark': i['mark'],
                      'message': i['message'],
                      'added_at': i['added_at']})
            return JsonResponse(reviewsForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetModerationReports(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            reports = list(Report.objects
                           .filter(is_moderated=None)
                           .select_related('added_by_user', 'page')
                           .values('id', 'page__id', 'page__name', 'page__url', 'message', 'added_at', 'added_by_user', 'added_by_user__username'))
            reportsForModerate = []
            for i in reports:
                reportsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'user': {'id': i['added_by_user'],
                              'username': i['added_by_user__username']},
                     'message': i['message'],
                     'added_at': i['added_at']})
            return JsonResponse(reportsForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class Moderate(generics.GenericAPIView):
    permission_classes = [IsAdminUser]


    def patch(self, request, category, id, *args, **kwargs):
        try:
            data = getData(request)
            user = request.user
            if data['action'] not in ['accept', 'reject', 'delete', 'revise']:
                return JsonResponse({'detail': 'Invalid action'}, status=400)
            if category == 'page':
                page = Page.objects.get(id=id)
                if data['action'] == 'accept':
                    page.is_moderated = True
                    page.is_checking = True
                    page.moderated_by_user_id = user.id
                    page.save()
                elif data['action'] == 'reject':
                    page.is_moderated = False
                    page.is_checking = False
                    page.moderated_by_user_id = user.id
                    page.save()
                elif data['action'] == 'revise':
                    page.is_moderated = None
                    page.is_checking = False
                    page.moderated_by_user_id = None
                    page.save()
                elif data['action'] == 'delete':
                    page.delete()
                return JsonResponse({'success': True})
            elif category == 'review':
                review = Review.objects.get(id=id)
                if data['action'] == 'accept':
                    review.is_moderated = True
                    review.is_published = True
                    review.moderated_by_user_id = user.id
                    review.save()
                elif data['action'] == 'reject':
                    review.is_moderated = False
                    review.is_published = False
                    review.moderated_by_user_id = user.id
                    review.save()
                elif data['action'] == 'revise':
                    review.is_moderated = None
                    review.is_published = False
                    review.moderated_by_user_id = None
                    review.save()
                elif data['action'] == 'delete':
                    review.delete()
                return JsonResponse({'success': True})
            elif category == 'report':
                report = Report.objects.get(id=id)
                if data['action'] == 'accept':
                    report.is_moderated = True
                    report.is_published = True
                    report.moderated_by_user_id = user.id
                    report.save()
                elif data['action'] == 'reject':
                    report.is_moderated = False
                    report.is_published = False
                    report.moderated_by_user_id = user.id
                    report.save()
                elif data['action'] == 'revise':
                    report.is_moderated = None
                    report.is_published = False
                    report.moderated_by_user_id = None
                    report.save()
                elif data['action'] == 'delete':
                    report.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'detail': 'Invalid category'}, status=400)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)

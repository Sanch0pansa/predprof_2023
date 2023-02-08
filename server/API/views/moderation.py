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
                                         'added_by_user': {'id': i['added_by_user'],
                                                           'username': i['added_by_user__username']}})
            return JsonResponse(pagesForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetRejectedModerationPages(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            pages = list(Page.objects
                         .filter(is_moderated=False)
                         .select_related('added_by_user', 'moderated_by_user')
                         .values('id', 'name', 'description', 'url', 'moderated_by_user', 'moderated_by_user__username',
                                 'added_by_user', 'added_by_user__username'))
            pagesForModerate = []
            for i in pages:
                pagesForModerate.append({'id': i['id'],
                                         'name': i['name'],
                                         'description': i['description'],
                                         'url': i['url'],
                                         'moderated_by_user': {'id': i['moderated_by_user'],
                                                               'username': i['moderated_by_user__username']},
                                         'added_by_user': {'id': i['added_by_user'],
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
                           .values('id', 'page__id', 'page__name', 'page__url', 'mark', 'message', 'added_at',
                                   'added_by_user', 'added_by_user__username'))
            reviewsForModerate = []
            for i in reviews:
                reviewsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'mark': i['mark'],
                     'message': i['message'],
                     'added_at': i['added_at'],
                     'added_by_user': {'id': i['added_by_user'],
                                       'username': i['added_by_user__username']}})
            return JsonResponse(reviewsForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetRejectedModerationReviews(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            reviews = list(Review.objects
                           .filter(is_moderated=False)
                           .select_related('added_by_user', 'moderated_by_user', 'page')
                           .values('id', 'moderated_by_user', 'moderated_by_user__username',
                                   'page__id', 'page__name', 'page__url', 'mark', 'message', 'added_at',
                                   'added_by_user', 'added_by_user__username'))
            reviewsForModerate = []
            for i in reviews:
                reviewsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'mark': i['mark'],
                     'message': i['message'],
                     'added_at': i['added_at'],
                     'moderated_by_user': {'id': i['moderated_by_user'],
                                           'username': i['moderated_by_user__username']},
                     'added_by_user': {'id': i['added_by_user'],
                                       'username': i['added_by_user__username']}})
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
                           .values('id', 'page__id', 'page__name', 'page__url', 'message', 'added_at', 'added_by_user',
                                   'added_by_user__username'))
            reportsForModerate = []
            for i in reports:
                reportsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'added_by_user': {'id': i['added_by_user'],
                                       'username': i['added_by_user__username']},
                     'message': i['message'],
                     'added_at': i['added_at']})
            return JsonResponse(reportsForModerate, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)


class GetRejectedModerationReports(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            reports = list(Report.objects
                           .filter(is_moderated=False)
                           .select_related('added_by_user', 'moderated_by_user', 'page')
                           .values('id', 'moderated_by_user', 'moderated_by_user__username', 'page__id', 'page__name',
                                   'page__url', 'message', 'added_at', 'added_by_user', 'added_by_user__username'))
            reportsForModerate = []
            for i in reports:
                reportsForModerate.append(
                    {'id': i['id'],
                     'page': {'id': i['page__id'],
                              'name': i['page__name']},
                     'message': i['message'],
                     'added_at': i['added_at'],
                     'added_by_user': {'id': i['added_by_user'],
                                       'username': i['added_by_user__username']},
                     'moderated_by_user': {'id': i['moderated_by_user'],
                                           'username': i['moderated_by_user__username']}})
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
                category = Page.objects.get(id=id)
            elif category == 'review':
                category = Review.objects.get(id=id)
            elif category == 'report':
                category = Report.objects.get(id=id)
            else:
                return JsonResponse({'detail': 'Invalid category'}, status=400)

            if data['action'] == 'accept':
                category.is_moderated = True
                category.is_published = True
                category.is_checking = True
                category.moderated_by_user_id = user.id
                category.save()
            elif data['action'] == 'reject':
                category.is_moderated = False
                category.is_published = False
                category.is_checking = False
                category.moderated_by_user_id = user.id
                category.save()
            elif data['action'] == 'revise':
                category.is_moderated = None
                category.is_published = False
                category.is_checking = False
                category.moderated_by_user_id = None
                category.save()
            elif data['action'] == 'delete':
                category.delete()
            return JsonResponse({'success': True})
        except Exception as ex:
            print(ex)
            return JsonResponse({'detail': 'Exception'}, status=404)

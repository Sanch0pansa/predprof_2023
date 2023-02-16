from rest_framework import generics
from API.models import User, Subscription, Review, Report
from django.http import JsonResponse
from API.serializers.user import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from API.permissions import IsAdmin
from rest_framework.authtoken.models import Token
from django.utils import timezone
from random import seed, randint
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import BaseUserManager
from API.funcs import getData
from django.core.exceptions import ValidationError


class UserCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data is None:
                return JsonResponse({'errors': {'email': ['Это поле не может быть пустым.'],
                                                'username': ['Это поле не может быть пустым.'],
                                                'password': ['Это поле не может быть пустым.']}}, status=400,
                                    safe=False)
            user = User(username=data['username'], email=BaseUserManager.normalize_email(data['email']),
                        password=data['password'])
            try:
                user.full_clean()
            except ValidationError:
                errors = dict(ex)
                if 'username' in errors:
                    errors['username'][0] = errors['username'][0].replace('Username', 'именем пользователя')
                if 'email' in errors:
                    errors['email'][0] = errors['email'][0].replace('таким Email', 'такой почтой')
                if 'password' in errors:
                    errors['password'][0] = errors['password'][0].replace('значение', 'пароль').replace('это', '')
                return JsonResponse({'errors': errors}, status=400, safe=False)
            user.set_password(data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'email': user.email, 'username': user.username, 'token': token.key})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class UserLogView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            if data['login'] == '' and data['password'] == '':
                return JsonResponse({'errors': {'login': ['Это поле не может быть пустым.'],
                                                'password': ['Это поле не может быть пустым.']}}, status=400,
                                    safe=False)
            elif data['login'] == '':
                return JsonResponse({'errors': {'login': ['Это поле не может быть пустым.']}}, status=400, safe=False)
            elif data['password'] == '':
                return JsonResponse({'errors': {'password': ['Это поле не может быть пустым.']}}, status=400,
                                    safe=False)
            try:
                user = User.objects.get(username=data['login'])
            except Exception:
                try:
                    user = User.objects.get(email=data['login'])
                except Exception:
                    return JsonResponse(
                        {'errors': {'non_field_errors': ['Невозможно войти с предоставленными учетными данными.']}},
                        status=400)
            if user.check_password(data['password']):
                try:
                    token = Token.objects.get(user=user)
                except Exception:
                    token = Token.objects.create(user=user)
                return JsonResponse({'auth_token': token.key})
            else:
                return JsonResponse(
                    {'errors': {'non_field_errors': ['Невозможно войти с предоставленными учетными данными.']}},
                    status=400)
        except Exception:
            return JsonResponse({'errors': str(ex)}, status=400, safe=False)

    def get(self, request):
        try:
            request.user.auth_token.delete()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=500)

class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GenerateTelegramCode(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            timeNow = timezone.now()
            codeTime = user.telegram_verification_code_date
            if user.telegram_verification_code_date is not None and codeTime > timeNow:
                return JsonResponse({'detail': 'Время действия кода ещё не истекло',
                                     'remain_time': (codeTime - timeNow).seconds,
                                     'telegram_verification_code': user.telegram_verification_code})
            elif user.telegram_id is not None:
                return JsonResponse({'detail': 'Телеграм уже привязан к аккаунту'})
            else:
                seed(int(str(int(datetime.timestamp(timezone.localtime()))) + str(user.id)))
                while True:
                    try:
                        user.telegram_verification_code = randint(100000, 999999)
                    except Exception:
                        continue
                    else:
                        break
                user.telegram_verification_code_date = (timezone.now() + timedelta(minutes=5))
                user.save()
                codeTime = user.telegram_verification_code_date
                return JsonResponse({'telegram_verification_code': user.telegram_verification_code,
                                     'remain_time': (codeTime - timeNow).seconds})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class ShowMe(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.role_id == 1:
                is_moderator = True
                is_admin = True
            elif user.role_id == 2:
                is_moderator = True
                is_admin = False
            else:
                is_moderator = False
                is_admin = False
            return JsonResponse({'username': user.username,
                                 'email': user.email,
                                 'telegram_id': user.telegram_id,
                                 'role': user.role.name,
                                 'is_moderator': is_moderator,
                                 'is_admin': is_admin})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class ChangePersonalData(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            is_password = 'password' in data
            if check_password(data['current_password'], user.password):
                if user.username != data['username']:
                    user.username = data['username']
                if user.email != data['email']:
                    user.email = BaseUserManager.normalize_email(data['email'])
                if is_password:
                    if not check_password(user.password, data['password']):
                        user.password = data['password']
                try:
                    user.validate_unique()
                except ValidationError:
                    errors = dict(ex)
                    if 'password' in errors:
                        errors['password'][0] = errors['password'][0].replace('значение', 'пароль').replace('это', '')
                    if 'username' in errors:
                        errors['username'][0] = errors['username'][0].replace('Username', 'именем пользователя')
                    if 'email' in errors:
                        errors['email'][0] = errors['email'][0].replace('таким Email', 'такой почтой')
                    return JsonResponse({'errors': errors}, status=400)
                if is_password:
                    user.set_password(data['password'])
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': {'current_password': ['Неправильный пароль']}}, status=400)
        except Exception:
            return JsonResponse({'success': False}, status=500)


class UnlinkTelegram(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user = User.objects.get(telegram_id=user.telegram_id)
            user.telegram_id = None
            user.save()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'detail': False}, status=500)


class UserInfo(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, id):
        try:
            subscriptions = Subscription.objects.only('id').filter(user=id).count()
            reports = Report.objects.only('id').filter(added_by_user=id).count()
            reviews = Review.objects.only('id').filter(added_by_user=id).count()
            joined = list(User.objects.filter(id=id).values('date_joined'))[0]['date_joined']
            return JsonResponse(
                {'reviews': reviews, 'reports': reports, 'subscriptions': subscriptions, 'joined': joined})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class UserReports(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            result = []
            reports = Report.objects.filter(added_by_user_id=user.id) \
                .select_related('page') \
                .order_by('-id') \
                .values('id', 'page', 'page__name', 'message', 'added_at', 'is_moderated')
            for i in reports:
                if i['is_moderated'] is None:
                    status = 'moderation'
                elif i['is_moderated']:
                    status = 'accepted'
                else:
                    status = 'rejected'
                result.append({'id': i['id'],
                               'page': {'id': i['page'],
                                        'name': i['page__name']},
                               'message': i['message'],
                               'added_at': i['added_at'],
                               'status': status})
            return JsonResponse(result, safe=False)
        except Exception:
            return JsonResponse({'success': False}, status=500)

    def delete(self, request, id):
        try:
            report = Report.objects.get(id=id)
            report.delete()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=500)


class UserReviews(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            result = []
            reviews = Review.objects.filter(added_by_user_id=user.id) \
                .select_related('page') \
                .order_by('-id') \
                .values('id', 'page', 'page__name', 'message', 'mark', 'added_at', 'is_moderated')
            for i in reviews:
                if i['is_moderated'] is None:
                    status = 'moderation'
                elif i['is_moderated']:
                    status = 'accepted'
                else:
                    status = 'rejected'
                result.append({'id': i['id'],
                               'page': {'id': i['page'],
                                        'name': i['page__name']},
                               'message': i['message'],
                               'mark': i['mark'],
                               'added_at': i['added_at'],
                               'status': status})
            return JsonResponse(result, safe=False)
        except Exception:
            return JsonResponse({'success': False}, status=500)

    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id)
            review.delete()
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False}, status=500)

from rest_framework import generics
from API.models import User, Subscription,Review, Report
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
            except ValidationError as ex:
                errors = dict(ex)
                if 'username' in errors and 'Username' in errors['username'][0]:
                    errors['username'][0] = errors['username'][0].replace('Username', 'именем пользователя')
                if 'email' in errors and 'Email' in errors['email'][0]:
                    errors['email'][0] = errors['email'][0].replace('таким Email', 'такой почтой')
                return JsonResponse({'errors': errors}, status=400, safe=False)
            user.set_password(data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'email': user.email, 'username': user.username, 'token': token.key})
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class UserLoginView(generics.GenericAPIView):
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
        except Exception as ex:
            return JsonResponse({'errors': str(ex)}, status=400, safe=False)


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
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


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
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class SetNewPassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            if check_password(data['current_password'], user.password):
                if check_password(data['new_password'], user.password):
                    return JsonResponse({'errors': {'new_password': ['Новый пароль совпадает со старым']}}, status=400)
                user.password = data['new_password']
                try:
                    user.clean_fields()
                except ValidationError as ex:
                    return JsonResponse({'errors': dict(ex)})
                user.set_password(data['new_password'])
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': {'password': ['Неправильный пароль']}}, status=400)
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)


class SetNewUsername(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            if check_password(data['current_password'], user.password):
                if user.username == data['new_username']:
                    return JsonResponse({'errors': {'new_username': ['Новое имя пользователя совпадает со старым']}}, status=400)
                user.username = data['new_username']
                try:
                    user.clean_fields()
                except ValidationError as ex:
                    return JsonResponse({'errors': dict(ex)})
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': {'password': ['Неправильный пароль']}}, status=400)
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)


class SetNewEmail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            if check_password(data['current_password'], user.password):
                if user.email == data['new_email']:
                    return JsonResponse({'errors': {'new_email': ['Новая почта совпадает со старой']}})
                user.email = BaseUserManager.normalize_email(data['new_email'])
                try:
                    user.clean_fields()
                except ValidationError as ex:
                    return JsonResponse({'errors': dict(ex)}, status=400)
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': {'password': ['Неправильный пароль']}}, status=400)
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)


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
        except Exception as ex:
            return JsonResponse({'detail': False}, status=404)


class UserInfo(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, id):
        try:
            subscriptions = Subscription.objects.only('id').filter(user=id).count()
            reports = Report.objects.only('id').filter(added_by_user=id).count()
            reviews = Review.objects.only('id').filter(added_by_user=id).count()
            joined = list(User.objects.filter(id=id).values('date_joined'))[0]['date_joined']
            return JsonResponse({'reviews': reviews, 'reports': reports, 'subscriptions': subscriptions, 'joined': joined})
        except Exception:
            return JsonResponse({'success': False}, status=404)
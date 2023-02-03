from rest_framework import generics
from API.models import User
from django.http import JsonResponse
from API.serializers.user import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
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
            user = User(username=data['username'], email=BaseUserManager.normalize_email(data['email']), password=data['password'])
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
            if data is None:
                return JsonResponse({'errors': {'login': ['Это поле не может быть пустым.'],
                                                'password': ['Это поле не может быть пустым.']}}, status=400,
                                    safe=False)
            elif 'login' not in data:
                return JsonResponse({'errors': {'login': ['Это поле не может быть пустым.']}}, status=400, safe=False)
            elif 'password' not in data:
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
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GenerateTelegramCode(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

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
            return JsonResponse({'username': user.username, 'email': user.email, 'telegram_id': user.telegram_id})
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
                user.set_password(data['new_password'])
                user.save()
                return JsonResponse({'detail': 'Пароль изменён'})
            else:
                return JsonResponse({'detail': 'Неверный пароль'})
        except Exception:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


class SetNewEmail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = getData(request)
            if check_password(data['current_password'], user.password):
                user.email = data['new_email']
                user.save()
                return JsonResponse({'detail': 'Почта изменена'})
            else:
                return JsonResponse({'detail': 'Неверный пароль'})
        except Exception:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)

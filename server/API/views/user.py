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
from API.funcs import getData

class UserCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = getData(request)
            user = User(email=data['email'], username=data['username'])
            user.set_password(data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'email': user.email, 'username': user.username, 'token': token.key})
        except Exception as ex:
            return JsonResponse({'errors': {'non_field_errors': [str(ex)]}}, status=400)


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

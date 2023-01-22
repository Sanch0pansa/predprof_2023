from rest_framework import generics
from API.models import User
from django.http import JsonResponse
from API.serializers.user import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.utils import timezone
from random import seed, randint
from datetime import datetime, timedelta


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GenerateTelegramCode(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.user
        if data.telegram_verification_code_date is not None and data.telegram_verification_code_date > timezone.now():
            return JsonResponse('Время действия кода ещё не истекло', safe=False)
        elif data.telegram_id != None:
            return JsonResponse('Телеграм уже привязан к аккаунту', safe=False)
        else:
            seed(int(str(int(datetime.timestamp(timezone.localtime()))) + str(data.id)))
            while True:
                try:
                    data.telegram_verification_code = randint(100000, 999999)
                except Exception:
                    continue
                else:
                    break
            data.telegram_verification_code_date = (timezone.now() + timedelta(minutes=5))
            data.save()
            return JsonResponse({'telegram_verification_code': data.telegram_verification_code})

from django.urls import path
from API.views import user

urlpatterns = [
    path('auth/user/registration/', user.UserCreateView.as_view()),
    path('auth/user/login/', user.UserLoginView.as_view()),
    path('user/set_new_password/', user.SetNewPassword.as_view()),
    path('user/set_new_email/', user.SetNewEmail.as_view()),
    path('user/generate_telegram_code/', user.GenerateTelegramCode.as_view()),
    path('user/unlink_telegram/', user.UnlinkTelegram.as_view()),
    path('user/me/', user.ShowMe.as_view()),
    path('user/list/', user.UserListView.as_view()),
    path('user/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view()),
]

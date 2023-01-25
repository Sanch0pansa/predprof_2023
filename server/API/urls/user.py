from django.urls import path
from API.views import user
from rest_framework.authtoken import views as authViews


urlpatterns = [
    path('user/list/', user.UserListView.as_view()),
    path('user/me/', user.ShowMe.as_view()),
    path('user/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view()),
    path('user/generate_telegram_code/', user.GenerateTelegramCode.as_view()),
    path('user/set_new_password/', user.SetNewPassword.as_view()),
    path('user/set_new_email/', user.SetNewEmail.as_view()),
]
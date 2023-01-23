from django.urls import path
from API.views import user
from rest_framework.authtoken import views as authViews


urlpatterns = [
    path('user/list/', user.UserListView.as_view()),
    path('user/me/', user.ShowMe.as_view()),
    # path('user/register/', user.UserCreateView.as_view()),
    # path('user/login/', authViews.obtain_auth_token),
    path('user/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view()),
    path('user/generate_telegram_code/', user.GenerateTelegramCode.as_view())
]
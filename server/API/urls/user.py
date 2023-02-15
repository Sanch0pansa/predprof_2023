from django.urls import path
from API.views import user

urlpatterns = [
    path('auth/user/registration/', user.UserCreateView.as_view()),
    path('auth/user/login/', user.UserLoginView.as_view()),
    path('user/change_account_info/', user.ChangePersonalData.as_view()),
    path('user/generate_telegram_code/', user.GenerateTelegramCode.as_view()),
    path('user/unlink_telegram/', user.UnlinkTelegram.as_view()),
    path('user/me/', user.ShowMe.as_view()),
    path('user/list/', user.UserListView.as_view()),
    path('user/retrive/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view()),
    path('user/<int:id>/', user.UserInfo.as_view()),
    path('user/report/', user.UserReports.as_view()),
    path('user/report/<int:id>/', user.UserReports.as_view()),
    path('user/review/', user.UserReviews.as_view()),
    path('user/review/<int:id>/', user.UserReviews.as_view())
]

from django.urls import path
from API.views import user

urlpatterns = [
    path('user/', user.UserListCreateView.as_view()),
    path('user/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view()),
    path('user/verify_code_gen/', user.VerifyCodeGen.as_view())
]
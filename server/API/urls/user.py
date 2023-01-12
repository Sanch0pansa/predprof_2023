from django.urls import path
from API.views import user

urlpatterns = [
    path('user/', user.UserListCreateView.as_view()),
    path('user/<int:pk>/', user.UserRetrieveUpdateDestroyView.as_view())
]
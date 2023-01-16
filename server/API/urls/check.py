from django.urls import path
from API.views import check

urlpatterns = [
    path('check/', check.CheckListCreateView.as_view()),
    path('check/<int:pk>/', check.CheckRetrieveUpdateDestroyView.as_view())
]
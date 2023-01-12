from django.urls import path
from API.views import page

urlpatterns = [
    path('page/', page.PageListCreateView.as_view()),
    path('page/<int:pk>/', page.PageRetrieveUpdateDestroyView.as_view())
]
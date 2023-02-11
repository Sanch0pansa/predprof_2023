from django.urls import path
from API.views import review

urlpatterns = [
    path('review/', review.ReviewListCreateView.as_view()),
    path('review/<int:pk>/', review.ReviewRetrieveUpdateDestroyView.as_view())
]

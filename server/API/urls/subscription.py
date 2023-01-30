from django.urls import path
from API.views import subscription

urlpatterns = [
    path('subscription/', subscription.SubscriptionListCreateView.as_view()),
    path('subscription/<int:pk>/', subscription.SubscriptionRetrieveUpdateDestroyView.as_view())
]
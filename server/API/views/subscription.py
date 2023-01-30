from rest_framework import generics
from API.models import Subscription
from API.serializers.subscription import SubscriptionSerializer

class SubscriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
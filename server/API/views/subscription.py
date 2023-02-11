from rest_framework import generics
from API.models import Subscription
from API.serializers.subscription import SubscriptionSerializer
from API.permissions import IsAdmin


class SubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

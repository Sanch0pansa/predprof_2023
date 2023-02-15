from rest_framework import generics
from API.models import Review
from API.serializers.review import ReviewSerializer
from API.permissions import IsAdmin


class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

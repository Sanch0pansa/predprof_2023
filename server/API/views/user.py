from rest_framework import generics
from API.models import User
from API.serializers.user import UserRetrieveUpdateDestroySerializer, UserCreateListSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserCreateListSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRetrieveUpdateDestroySerializer
    queryset = User.objects.all()
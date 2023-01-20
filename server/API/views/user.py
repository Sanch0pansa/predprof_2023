from rest_framework import generics
from API.models import User
from API.serializers.user import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class VerifyCodeGen(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass
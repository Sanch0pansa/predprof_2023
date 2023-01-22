from rest_framework import generics
from API.models import User
from API.serializers.user import UserSerializer
from rest_framework import permissions

class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class VerifyCodeGen(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass
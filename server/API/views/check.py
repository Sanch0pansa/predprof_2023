from rest_framework import generics
from API.models import Check
from API.serializers.check import CheckSerializer

class CheckListCreateView(generics.ListCreateAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()
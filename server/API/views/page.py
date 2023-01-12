from rest_framework import generics
from API.models import Page
from API.serializers.page import PageRetrieveUpdateDestroySerializer, PageCreateListSerializer


class PageListCreateView(generics.ListCreateAPIView):
    serializer_class = PageCreateListSerializer
    queryset = Page.objects.all()


class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageRetrieveUpdateDestroySerializer
    queryset = Page.objects.all()
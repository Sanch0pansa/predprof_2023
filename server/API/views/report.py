from rest_framework import generics
from API.models import Report
from API.serializers.report import ReportSerializer

class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
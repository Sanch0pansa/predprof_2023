from rest_framework import generics
from API.models import Report
from API.serializers.report import ReportSerializer
from API.permissions import IsAdmin


class ReportListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

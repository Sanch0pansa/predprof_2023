from django.urls import path
from API.views import report

urlpatterns = [
    path('report/', report.ReportListCreateView.as_view()),
    path('report/<int:pk>/', report.ReportRetrieveUpdateDestroyView.as_view())
]

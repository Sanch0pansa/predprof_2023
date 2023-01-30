from django.urls import path
from API.views import checker

urlpatterns = [
    path('checker/get_pages_for_check/', checker.GetPagesForCheck.as_view()),
    path('checker/check/', checker.CheckCreateView.as_view())
]
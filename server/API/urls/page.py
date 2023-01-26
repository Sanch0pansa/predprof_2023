from django.urls import path
from API.views import page

urlpatterns = [
    path('page/', page.PageListCreateView.as_view()),
    path('page/<int:pk>/', page.PageRetrieveUpdateDestroyView.as_view()),
    path('page/get_popular_pages/', page.GetPopularPages.as_view()),
    path('page/get_statistic/', page.GetSiteStats.as_view()),
    path('page/get_checking_pages/', page.GetCheckingPages.as_view()),
    path('page/get_account_data/', page.GetAccountData.as_view())
]
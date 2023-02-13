from django.urls import path
from API.views import page

urlpatterns = [
    path('page/', page.PageCreate.as_view()),
    path('pageR/<int:pk>/', page.PageRetrieveUpdateDestroyView.as_view()),
    path('page/get_popular_pages/', page.GetPopularPages.as_view()),
    path('page/get_statistic/', page.GetSiteStats.as_view()),
    path('page/get_checking_pages/', page.GetCheckingPages.as_view()),
    path('page/account/data/', page.GetAccountData.as_view()),
    path('page/<int:id>/checks/', page.PageChecks.as_view()),
    path('page/<int:id>/reviews/', page.PageReviews.as_view()),
    path('page/<int:id>/reports/', page.PageReports.as_view()),
    path('page/<int:id>/subscription/', page.Subscriptions.as_view()),
    path('page/<int:id>/', page.GetPageData.as_view()),
    path('page/account/events/', page.Events.as_view())
]

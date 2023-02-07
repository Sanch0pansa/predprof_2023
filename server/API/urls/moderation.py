from django.urls import path
from API.views import moderation

urlpatterns = [
    path('moderation/get_categories/', moderation.GetModerateCategories.as_view()),
    path('moderation/pages/', moderation.GetModerationPages.as_view()),
    path('moderation/reviews/', moderation.GetModerationReviews.as_view()),
    path('moderation/reports/', moderation.GetModerationReports.as_view()),
    path('moderation/moderate/<str:category>/<int:id>/', moderation.Moderate.as_view())
]
from django.urls import path
from API.views import bot

urlpatterns = [
    path('bot/', bot.get_messages.as_view()),
]
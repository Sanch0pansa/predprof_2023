from django.urls import path
from API.views import bot

urlpatterns = [
    path('bot/get_bot_messages', bot.GetBotMessages.as_view()),
]
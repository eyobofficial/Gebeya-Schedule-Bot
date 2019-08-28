from django.urls import path

from .views import TelegramBotView

app_name = 'bot'

urlpatterns = [
    path('', TelegramBotView.as_view(), name='telegram')
]

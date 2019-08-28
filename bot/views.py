import telegram

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser

from .bots import TelegramBot


User = get_user_model()


class TelegramBotView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = request.data
        self.bot = TelegramBot(context=context)
        user, _ = User.objects.get_or_create(
            username=self.bot.sender['username'],
            defaults={
                'telegram_id': self.bot.sender['id'],
                'first_name': self.bot.sender['first_name']
            }
        )
        user.access_count += 1
        user.save()
        self.bot.dispatcher(user)
        return Response(status=status.HTTP_200_OK)




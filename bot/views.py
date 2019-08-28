import telegram

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .bots import TelegramBot
from .models import TelegramUser as User


class TelegramBotView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = request.data
        self.bot = TelegramBot(context=context)
        user, _ = User.objects.get_or_create(
            id=self.bot.sender['id'],
            defaults={
                'first_name': self.bot.sender['first_name'],
                'last_name': self.bot.sender.get('last_name', ''),
                'username': self.bot.sender.get('username', ''),
                'is_bot': self.bot.sender.get('is_bot', False)
            }
        )
        user.access_count += 1
        user.save()
        self.bot.dispatcher(user)
        return Response(status=status.HTTP_200_OK)




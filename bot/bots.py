import telegram

from django.conf import settings

from schedules.models import Schedule, Track

from .constants import messages
from .models import TelegramUser as User


class TelegramBot:
    """
    Telegram Bot Handler.
    """

    def __init__(self, **kwargs):
        # Initialize telegram bot
        self.bot = telegram.Bot(settings.TELEGRAM_BOT_TOKEN)

        # Handle edited messages
        self.context = kwargs.get('context')
        self.data = self.context.get('message') or self.context.get('edited_message')

        # Get tracks and sessions
        self.tracks = Track.objects.values_list('title', flat=True)
        self.sessions = {s[0]: s[1] for s in User.SESSION_CHOICES}

        # Register commands
        self.commands = [
            'start', 'track', 'session',
            'today', 'tomorrow', 'week', 'month',
            'help', 'credits', 'me', 'about'
        ]

    @property
    def message(self):
        if self.data:
            return self.data['text'].strip()
        return

    @property
    def sender(self):
        if self.data:
            return self.data['from']
        return

    @property
    def chat_id(self):
        if self.data:
            return self.data['chat']['id']
        return

    def send_message(self, chat_id, text, keyboard=None):
        """
        Send message to a user with his/her telegram_id.
        """
        if keyboard:
            reply_markup = telegram.ReplyKeyboardMarkup(
                keyboard,
                on_time_keyboard=True,
                resize_keyboard=True
            )
        else:
            reply_markup=None

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    def reply(self, text, keyboard=None):
        """
        Reply to the user sent who sent the message.
        """
        if not self.chat_id:
            return
        self.send_message(chat_id=self.chat_id, text=text, keyboard=keyboard)

    def remove_keyboard(self, text):
        reply_markup = telegram.ReplyKeyboardRemove()
        self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    def dispatcher(self, user):
        """
        Dispatch user messages (commands and texts) to the right method.
        """
        message = f'Hi {user.first_name} 👋🏼\nDue to lack of access to the ' \
                   'schedules of all tracks, I am no longer able to tell you ' \
                   'your class programs. If you can think of any solution for ' \
                   'the problem, contact me @eyobofficial. Sorry for the ' \
                   'inconvenience 😔'
        self.reply(message)
        # if self.message.startswith('/'):
        #     command = self.message.lstrip('/')
        #     if command not in self.commands:
        #        self.reply("I don't know this command. Use /help to checkout my commands.")
        #     else:
        #         method = getattr(self, command)
        #         method(user=user)
        # else:
        #     self.response_handler(user)

    def start(self, **kwargs):
        user = kwargs.get('user')
        if not user.track:
            self.track()
        elif not user.session:
            self.session()
        else:
            message = messages.welcome_message.format(
                user.first_name, user.track, self.sessions[user.session].lower()
            )
            self.remove_keyboard(text=message)

    def track(self, **kwargs):
        text = f'Select your learning `track`.'
        keyboard = [
            ['Business Analyst'],
            ['UI/UX', 'Front-end'],
            ['Back-end', 'DevOps']
        ]
        self.reply(text=text, keyboard=keyboard)

    def session(self, **kwargs):
        text = 'Select your class `session` (day or evening).'
        keyboard = [
            ['Day'],
            ['Evening']
        ]
        self.reply(text=text, keyboard=keyboard)

    def today(self, **kwargs):
        """
        Send a message to the user with the list of today's class.
        """
        user = kwargs.get('user')
        if not user.track:
            self.reply(text=messages.track_missing)
        elif not user.session:
            self.reply(text=messages.session_missing)
        else:
            schedules = user.get_today_schedules()
            message = TelegramBot.format_schedules(schedules, context='today')
            self.reply(text=message)

    def tomorrow(self, **kwargs):
        """
        Send a message to the user with the list of tomorrow's class.
        """
        user = kwargs.get('user')
        if not user.track:
            self.reply(text=messages.track_missing)
        elif not user.session:
            self.reply(text=messages.session_missing)
        else:
            schedules = user.get_tomorrow_schedules()
            message = TelegramBot.format_schedules(schedules, context='tomorrow')
            self.reply(text=message)

    def week(self, **kwargs):
        """
        Send a message to the user with the list of 1 week class.
        """
        user = kwargs.get('user')
        if not user.track:
            self.reply(text=messages.track_missing)
        elif not user.session:
            self.reply(text=messages.session_missing)
        else:
            schedules = user.get_week_schedules()
            message = TelegramBot.format_schedules(schedules, context='this week')
            self.reply(text=message)

    def month(self, **kwargs):
        """
        Send a message to the user with the list of 1 month class.
        """
        user = kwargs.get('user')
        if not user.track:
            self.reply(text=messages.track_missing)
        elif not user.session:
            self.reply(text=messages.session_missing)
        else:
            schedules = user.get_month_schedules()
            message = TelegramBot.format_schedules(schedules, context='this month')
            self.reply(text=message)

    def help(self, **kwargs):
        """
        Send help message
        """
        self.reply(text=messages.help_message)

    def me(self, **kwargs):
        """
        Send message about my account detail.
        """
        user = kwargs.get('user')
        track = user.track or "Unknown. Use /track to set it."
        session = self.sessions.get(user.session) or "Unknown. Use /session to set it."
        message = messages.me.format(user.first_name, track, session)
        self.reply(text=message)

    def credits(self, **kwargs):
        """
        Get the list of contributors.
        """
        self.reply(text=messages.credits_message)

    def about(self, **kwargs):
        """
        Send a reply with a brief introduction of the bot.
        """
        self.reply(text=messages.about)

    def response_handler(self, user):
        """
        Handle the user response messages.
        """
        if self.message in self.tracks:
            self.set_user_track(user)
            self.start(user=user)

        elif self.message in self.sessions.values():
            self.set_user_session(user)
            self.start(user=user)
        else:
            self.start(user=user)

    def set_user_track(self, user):
        """
        Sets the sender's learning track.
        """
        for track in Track.objects.all():
            if track.title == self.message:
                user.track = track
                user.save()

    def set_user_session(self, user):
        """
        Sets the sender's class session (Date or Evening)
        """
        for key, value in self.sessions.items():
            if value == self.message:
                user.session = key
                user.save()

    @staticmethod
    def format_schedules(schedules, context):
        if schedules.count() == 0:
            message = f"You have no class {context.lower()}. Have fun 😁"
        else:
            message = f"*{context.upper()} SCHEDULES* \n\n"
            for schedule in schedules:
                message += f"{schedule.course.title} \n"
                message += f"📅 {schedule.date.strftime('%a %b %d, %Y')} \n"
                message += "🕒 {} - {} \n".format(
                    schedule.start_time.strftime('%I:%M %P'),
                    schedule.end_time.strftime('%I:%M %P')
                )
                if schedule.type == Schedule.MAKEUP:
                    message += "⚠️ *Makeup class* \n"
                message += "\n"
        return message



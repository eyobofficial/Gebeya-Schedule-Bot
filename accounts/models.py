from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from schedules.models import Track


class CustomUser(AbstractUser):

    # Sessions
    DAY = 'DAY'
    EVENING = 'EVE'
    SESSION_CHOICES = (
        (DAY, 'Day'),
        (EVENING, 'Evening')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    password = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        editable=False
    )
    telegram_id = models.BigIntegerField(null=True, blank=True)
    track = models.ForeignKey(
        Track,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    session = models.CharField(max_length=3, choices=SESSION_CHOICES, blank=True)
    access_count = models.IntegerField(default=0)
    is_manually_added = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_today_schedules(self):
        """
        Return a queryset of user's class schedules for today.
        """
        today = timezone.now()
        return self.track.schedules.filter(
            session=self.session,
            date=today
        ).order_by('start_time')

    def get_tomorrow_schedules(self):
        """
        Return a queryset of user's class schedules for tomorrow.
        """
        tomorrow = timezone.now() + timedelta(days=1)
        return self.track.schedules.filter(
            session=self.session,
            date=tomorrow
        ).order_by('start_time')

    def get_week_schedules(self):
        """
        Return a queryset of user's class schedules for 1 week.
        """
        today = timezone.now()
        week = timezone.now() + timedelta(weeks=1)
        return self.track.schedules.filter(
            session=self.session,
            date__gte=today,
            date__lte=week
        ).order_by('date', 'start_time')

    def get_month_schedules(self):
        """
        Return a queryset of user's class schedules for 1 month.
        """
        today = timezone.now()
        month = timezone.now() + timedelta(days=31)
        return self.track.schedules.filter(
            session=self.session,
            date__gte=today,
            date__lte=month
        ).order_by('date', 'start_time')

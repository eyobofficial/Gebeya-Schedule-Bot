from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from shared.views import BaseScheduleRuleView

from .models import ScheduleRule


class ScheduleRuleGenerateView(BaseScheduleRuleView):
    url = 'admin:schedules_schedulerule_change'
    model = ScheduleRule

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.generate()
        message = 'The schedules are generated.'
        messages.success(request, message)
        return redirect(reverse(self.url, args=(self.object.pk,)))

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView


@method_decorator(staff_member_required, name='dispatch')
class BaseScheduleRuleView(DetailView):
    url = None
    object = None

from datetime import timedelta
from django.utils.timezone import now
from request.models import Request
from request.plugins import set_count, Plugin
from request.tracking.models import Visitor, Visit
from request import settings
from request.traffic import modules


class ActiveVisitors(Plugin):
    def template_context(self):
        visitors = Visitor.objects.all().in_progress()
        since = now() - timedelta(**settings.VISIT_TIMEOUT)
        return {
            'since': since,
            'visitors': visitors,
        }


class VisitorTrafficInformation(Plugin):
    def template_context(self):
        return {
            'visitors': Visitor.objects.all(),
            'visits': Visit.objects.all(),
            'requests': Request.objects.all(),
        }

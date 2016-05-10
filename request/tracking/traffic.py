from django.utils.translation import ugettext_lazy as _
from request.traffic import Module
from request.tracking.models import Visit, Visitor


class UniqueVisit(Module):
    verbose_name = _('Unique Visit')
    verbose_name_plural = _('Unique Visits')

    def count(self, qs):
        return Visit.objects.filter(requests__in=qs).count()


class UniqueVisitor(Module):
    verbose_name = _('Unique Visitor')
    verbose_name_plural = _('Unique Visitor')

    def count(self, qs):
        return Visitor.objects.filter(visit__requests__in=qs).count()


class NewVisitor(Module):
    verbose_name = _('New visitors')
    verbose_name_plural = _('New visitors')

    def count(self, qs):
        return Visitor.objects.filter(visit__requests__in=qs).new().count()


class Singleton(Module):
    verbose_name = _('Singleton')
    verbose_name_plural = _('Singleton')

    def count(self, qs):
        return Visit.objects.filter(requests__in=qs).singleton().count()


class RepeatedVisitor(Module):
    verbose_name = _('Repeated visitor')
    verbose_name_plural = _('Repeated visitors')

    def count(self, qs):
        return Visitor.objects.filter(visit__requests__in=qs).repeated().count()

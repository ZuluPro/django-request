from user_agents import parse as ua_parse

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from request.models import Request
from request.tracking.managers import VisitorManager, VisitManager


@python_2_unicode_compatible
class Visitor(models.Model):
    key = models.CharField(max_length=100)
    first_time = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = VisitorManager()

    class Meta:
        app_label = 'tracking'
        verbose_name = _('visitor')
        verbose_name_plural = _('visitors')

    def __str__(self):
        return "#%s" % self.id

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visitor_change', args=(self.id,))

    def get_delete_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visitor_delete', args=(self.id,))

    @property
    def requests(self):
        ids = Visit.objects.filter(visitor=self)\
            .values_list('requests', flat=True)
        return Request.objects.filter(id__in=ids)

    def hits(self):
        return self.requests.count()

    def visits(self):
        return self.visit_set.count()

    @property
    def ips(self):
        return list(set(self.requests.values_list('ip', flat=True)))

    @property
    def last_time(self):
        try:
            return self.requests.order_by('-time')[0].time
        except IndexError:
            return None

    def recency(self):
        """Time between two last visits."""
        raise NotImplementedError("Not yet!")

    def in_progress(self):
        """Return boolean representing active state of visitor"""
        return Visitor.objects.filter(id=self.id).in_progress().exists()


@python_2_unicode_compatible
class Visit(models.Model):
    visitor = models.ForeignKey(Visitor)
    first_time = models.DateTimeField(auto_now_add=True, db_index=True)
    last_time = models.DateTimeField(auto_now=True, db_index=True)
    requests = models.ManyToManyField(Request)

    objects = VisitManager()

    class Meta:
        app_label = 'tracking'
        verbose_name = _('visit')
        verbose_name_plural = _('visits')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visit_change', args=(self.id,))

    def get_delete_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visit_delete', args=(self.id,))

    @property
    def ip(self):
        return self.requests.first().ip

    @property
    def ua(self):
        if not hasattr(self, '_ua'):
            self._ua = ua_parse(self.requests.first().user_agent)
        return self._ua

    @property
    def browser(self):
        return self.ua.browser.family

    @property
    def os(self):
        return self.ua.os.family

    @property
    def device(self):
        return self.ua.device.family

    def hits(self):
        return self.requests.count()

    def in_progress(self):
        """Return boolean representing active state of visit."""
        return Visit.objects.filter(id=self.id).in_progress().exists()

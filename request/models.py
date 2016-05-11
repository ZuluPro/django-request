from socket import gethostbyaddr
from datetime import timedelta

from user_agents import parse as ua_parse

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.sessions.backends.db import SessionStore

from request import settings
from request.managers import RequestManager
from request.utils import HTTP_STATUS_CODES, engines

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Request(models.Model):
    # Response infomation
    response = models.SmallIntegerField(_('response'), choices=HTTP_STATUS_CODES, default=200)

    # Request infomation
    method = models.CharField(_('method'), default='GET', max_length=7)
    path = models.CharField(_('path'), max_length=255)
    time = models.DateTimeField(_('time'), default=now, db_index=True)

    is_secure = models.BooleanField(_('is secure'), default=False)
    is_ajax = models.BooleanField(
        _('is ajax'),
        default=False,
        help_text=_('Wheather this request was used via javascript.'),
    )

    # User infomation
    ip = models.GenericIPAddressField(_('ip address'))
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('user'))
    referer = models.URLField(_('referer'), max_length=255, blank=True, null=True)
    user_agent = models.CharField(_('user agent'), max_length=255, blank=True, null=True, default='')
    language = models.CharField(_('language'), max_length=255, blank=True, null=True)

    objects = RequestManager()

    class Meta:
        app_label = 'request'
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        ordering = ('-time',)

    def __str__(self):
        return '[%s] %s %s %s' % (self.time, self.method, self.path, self.response)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:request_request_change', args=(self.id,))

    def get_user(self):
        return get_user_model().objects.get(pk=self.user_id)

    def _get_last_visit(self, visitor):
        from request.tracking.models import Visit
        timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
        visits = Visit.objects.filter(visitor=visitor,
                                      last_time__gte=timeout)
        if visits.exists():
            visit = visits[0]
            visit.last_time = now()
            visit.save()
        else:
            visit = Visit.objects.create(visitor=visitor)
        return visit

    def from_http_request(self, request, response=None, commit=True):
        # Request infomation
        self.method = request.method
        self.path = request.path[:255]

        self.is_secure = request.is_secure()
        self.is_ajax = request.is_ajax()

        # User infomation
        self.ip = request.META.get('REMOTE_ADDR', '')
        self.referer = request.META.get('HTTP_REFERER', '')[:255]
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        self.language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:255]

        if getattr(request, 'user', False):
            if request.user.is_authenticated():
                self.user = request.user

        if response:
            self.response = response.status_code

            if (response.status_code == 301) or (response.status_code == 302):
                self.redirect = response['Location']

        if commit:
            self.save()

        if settings.USE_TRACKING and response and commit:
            from request.tracking.models import Visitor
            if 'track_key' in request.COOKIES:
                track_key = request.COOKIES['track_key']
            else:
                if hasattr(request, 'session'):
                    track_key = request.session._get_or_create_session_key()
                else:
                    track_key = SessionStore()._get_new_session_key()
                response.cookies['track_key'] = track_key

            visitor, created = Visitor.objects.get_or_create(key=track_key)
            visit = self._get_last_visit(visitor)
            visit.requests.add(self)

    @property
    def ua(self):
        if not hasattr(self, '_ua'):
            self._ua = ua_parse(self.user_agent)
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

    @property
    def keywords(self):
        if not self.referer:
            return

        if not hasattr(self, '_keywords'):
            self._keywords = engines.resolve(self.referer)
        if self._keywords:
            return ' '.join(self._keywords[1]['keywords'].split('+'))

    @property
    def hostname(self):
        try:
            return gethostbyaddr(self.ip)[0]
        except Exception:  # socket.gaierror, socket.herror, etc
            return self.ip

    def save(self, *args, **kwargs):
        if not settings.REQUEST_LOG_IP:
            self.ip = settings.REQUEST_IP_DUMMY
        elif settings.REQUEST_ANONYMOUS_IP:
            parts = self.ip.split('.')[0:-1]
            parts.append('1')
            self.ip = '.'.join(parts)
        if not settings.REQUEST_LOG_USER:
            self.user = None

        super(Request, self).save(*args, **kwargs)

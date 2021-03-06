from django.conf import settings

if 'request.tracking' in settings.INSTALLED_APPS:
    DEFAULT_PLUGINS = (
        'request.tracking.plugins.VisitorTrafficInformation',
        'request.plugins.LatestRequests',
        'request.tracking.plugins.LatestVisits',
        'request.plugins.TopPaths',
        'request.plugins.TopErrorPaths',
        'request.plugins.TopReferrers',
        'request.plugins.TopSearchPhrases',
        'request.plugins.TopBrowsers',
        'request.tracking.plugins.ActiveVisitors',
    )
    DEFAULT_TRAFFIC_MODULES = (
        'request.tracking.traffic.UniqueVisitor',
        'request.tracking.traffic.UniqueVisit',
        'request.traffic.Hit',
        'request.tracking.traffic.NewVisitor',
        'request.tracking.traffic.Singleton',
        'request.tracking.traffic.RepeatedVisitor',
    )
else:
    DEFAULT_PLUGINS = (
        'request.plugins.TrafficInformation',
        'request.plugins.LatestRequests',
        'request.plugins.TopPaths',
        'request.plugins.TopErrorPaths',
        'request.plugins.TopReferrers',
        'request.plugins.TopSearchPhrases',
        'request.plugins.TopBrowsers',
    )
    DEFAULT_TRAFFIC_MODULES = (
        'request.traffic.UniqueVisitor',
        'request.traffic.UniqueVisit',
        'request.traffic.Hit',
    )
REQUEST_PLUGINS = getattr(settings, 'REQUEST_PLUGINS', DEFAULT_PLUGINS)
REQUEST_TRAFFIC_MODULES = getattr(settings, 'REQUEST_TRAFFIC_MODULES', DEFAULT_TRAFFIC_MODULES)

REQUEST_VALID_METHOD_NAMES = getattr(settings, 'REQUEST_VALID_METHOD_NAMES', ('get', 'post', 'put', 'delete', 'head', 'options', 'trace'))

REQUEST_ONLY_ERRORS = getattr(settings, 'REQUEST_ONLY_ERRORS', False)
REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_LOG_IP = getattr(settings, 'REQUEST_LOG_IP', True)
REQUEST_IP_DUMMY = getattr(settings, 'REQUEST_IP_DUMMY', "1.1.1.1")
REQUEST_ANONYMOUS_IP = getattr(settings, 'REQUEST_ANONYMOUS_IP', False)
REQUEST_LOG_USER = getattr(settings, 'REQUEST_LOG_USER', True)
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())
REQUEST_IGNORE_PATHS = getattr(settings, 'REQUEST_IGNORE_PATHS', tuple())
REQUEST_IGNORE_USER_AGENTS = getattr(settings, 'REQUEST_IGNORE_USER_AGENTS', tuple())

try:
    from django.http import HttpRequest
    from django.contrib.sites.shortcuts import get_current_site
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://{0}'.format(get_current_site(HttpRequest()).domain))
except:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://127.0.0.1')

USE_TRACKING = 'request.tracking' in settings.INSTALLED_APPS
VISIT_TIMEOUT = getattr(settings, 'REQUEST_VISIT_TIMEOUT', {'minutes': 30})

GEOIP_PATH = getattr(settings, 'GEOIP_PATH', None)

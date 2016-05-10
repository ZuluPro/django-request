from time import strptime
from datetime import datetime, timedelta, date as Date, time
from django.db import models
from django.utils.timezone import now
from request import settings


class VisitorQuerySet(models.query.QuerySet):
    def year(self, year):
        return self.filter(visit__requests__time__year=year).distinct()

    def month(self, year=None, month=None, month_format='%b', date=None):
        if not date:
            try:
                if year and month:
                    date = Date(*strptime(year + month, '%Y' + month_format)[:3])
                else:
                    raise TypeError('Request.objects.month() takes exactly 2 arguments')
            except ValueError:
                return

        # Calculate first and last day of month, for use in a date-range lookup.
        first_day = date.replace(day=1)
        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)

        lookup_kwargs = {
            'visit__requests__time__gte': first_day,
            'visit__requests__time__lt': last_day,
        }

        return self.filter(**lookup_kwargs).distinct()

    def week(self, year, week):
        try:
            date = Date(*strptime(year + '-0-' + week, '%Y-%w-%U')[:3])
        except ValueError:
            return

        # Calculate first and last day of week, for use in a date-range lookup.
        first_day = date
        last_day = date + timedelta(days=7)
        lookup_kwargs = {
            'visit__requests__time__gte': first_day,
            'visit__requests__time__lt': last_day,
        }

        return self.filter(**lookup_kwargs).distinct()

    def day(self, year=None, month=None, day=None, month_format='%b', day_format='%d', date=None):
        if not date:
            try:
                if year and month and day:
                    date = Date(*strptime(year + month + day, '%Y' + month_format + day_format)[:3])
                else:
                    raise TypeError('day() takes exactly 3 arguments')
            except ValueError:
                return

        return self.filter(visit__requests__time__range=(datetime.combine(date, time.min), datetime.combine(date, time.max))).distinct()

    def today(self):
        return self.day(date=Date.today())

    def this_year(self):
        return self.year(now().year)

    def this_month(self):
        return self.month(date=Date.today())

    def this_week(self):
        today = Date.today()
        return self.week(str(today.year), str(today.isocalendar()[1] - 1))

    def repeated(self):
        """Filter that has made at least two visits."""
        qs = self.annotate(visit_num=models.Count('visit'))
        return qs.filter(visit_num__gt=1).distinct()

    def new(self):
        """Filter that has not made any previous visits."""
        qs = self.annotate(visit_num=models.Count('visit'))
        return qs.filter(visit_num=1)

    def in_progress(self):
        """Filter that is currently visiting."""
        timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
        return self.filter(visit__requests__time__gte=timeout).distinct()


class VisitorManager(models.Manager):
    _queryset_class = VisitorQuerySet
    _queryset_proxy_methods = ['repeated', 'returned', 'new', 'in_progress']

    def __getattr__(self, attr, *args, **kwargs):
        if attr in self._queryset_proxy_methods:
            return getattr(self.get_query_set(), attr, None)
        super(VisitorManager, self).__getattr__(*args, **kwargs)


class VisitQuerySet(models.query.QuerySet):
    def year(self, year):
        return self.filter(requests__time__year=year).distinct()

    def month(self, year=None, month=None, month_format='%b', date=None):
        if not date:
            try:
                if year and month:
                    date = Date(*strptime(year + month, '%Y' + month_format)[:3])
                else:
                    raise TypeError('Request.objects.month() takes exactly 2 arguments')
            except ValueError:
                return

        # Calculate first and last day of month, for use in a date-range lookup.
        first_day = date.replace(day=1)
        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)

        lookup_kwargs = {
            'requests__time__gte': first_day,
            'requests__time__lt': last_day,
        }

        return self.filter(**lookup_kwargs).distinct()

    def week(self, year, week):
        try:
            date = Date(*strptime(year + '-0-' + week, '%Y-%w-%U')[:3])
        except ValueError:
            return

        # Calculate first and last day of week, for use in a date-range lookup.
        first_day = date
        last_day = date + timedelta(days=7)
        lookup_kwargs = {
            'requests__time__gte': first_day,
            'requests__time__lt': last_day,
        }

        return self.filter(**lookup_kwargs).distinct()

    def day(self, year=None, month=None, day=None, month_format='%b', day_format='%d', date=None):
        if not date:
            try:
                if year and month and day:
                    date = Date(*strptime(year + month + day, '%Y' + month_format + day_format)[:3])
                else:
                    raise TypeError('day() takes exactly 3 arguments')
            except ValueError:
                return

        return self.filter(requests__time__range=(datetime.combine(date, time.min), datetime.combine(date, time.max))).distinct()

    def today(self):
        return self.day(date=Date.today())

    def this_year(self):
        return self.year(now().year)

    def this_month(self):
        return self.month(date=Date.today())

    def this_week(self):
        today = Date.today()
        return self.week(str(today.year), str(today.isocalendar()[1] - 1))

    def in_progress(self):
        """Filter that in progress."""
        timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
        return self.filter(requests__time__gte=timeout)

    def singleton(self):
        """Filter that in which only a single page is visited."""
        qs = self.annotate(request_num=models.Count('requests'))
        return qs.filter(request_num=1)


class VisitManager(models.Manager):
    _queryset_class = VisitQuerySet
    _queryset_proxy_methods = ['in_progress', 'singleton']

    def __getattr__(self, attr, *args, **kwargs):
        if attr in self._queryset_proxy_methods:
            return getattr(self.get_query_set(), attr, None)
        super(VisitManager, self).__getattr__(*args, **kwargs)

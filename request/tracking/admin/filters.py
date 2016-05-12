from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class CountListFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ('1', _('1')),
            ('>1', _('More than 1')),
            ('>=5', _('More than 5')),
            ('>=10', _('More than 10')),
            ('>=50', _('More than 50')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        field = self.field
        if value.startswith('>') or value.startswith('<'):
            field += '__gt' if value.startswith('>') else '__lt'
            value = value[1:]
            if value.startswith('='):
                field += 'e'
                value = value[1:]
        filters = {field: value}
        return queryset.filter(**filters)


class VisitorHitsListFilter(CountListFilter):
    title = _("Hits")
    parameter_name = "hits"
    field = 'visit__requests__count'


class VisitorVisitsListFilter(CountListFilter):
    title = _("Visits")
    parameter_name = "visits"
    field = 'visit__count'


class VisitHitsListFilter(CountListFilter):
    title = _("Hits")
    parameter_name = "hits"
    field = 'requests__count'

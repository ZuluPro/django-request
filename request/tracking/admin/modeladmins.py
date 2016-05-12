from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from request.tracking.models import Visitor, Visit
from request.tracking.admin import filters


class VisitorAdmin(admin.ModelAdmin):
    change_form_template = 'request/tracking/visitor_change_form.html'
    fieldsets = (
        (_('Visitor'), {'fields': ('key',)},),
    )
    readonly_fields = ('key',)

    date_hierarchy = 'first_time'
    list_display = ('key', 'hit_count', 'visit_count', 'first_time', 'last_time')
    list_filter = ('first_time', filters.VisitorHitsListFilter, filters.VisitorVisitsListFilter)

    def get_queryset(self, request):
        qs = super(VisitorAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('visit__requests'),
                         models.Count('visit', distinct=True),
                         models.Max('visit__requests__time'))
        return qs

    def hit_count(self, obj):
        return obj.visit__requests__count
    hit_count.admin_order_field = 'visit__requests__count'
    hit_count.short_description = _('Hits')

    # TODO: Why obj.visit__count doesn't work
    def visit_count(self, obj):
        return obj.visits()
    visit_count.admin_order_field = 'visit__count'
    visit_count.short_description = _('Visits')

    def last_time(self, obj):
        return obj.visit__requests__time__max
    last_time.admin_order_field = 'visit__requests__time__max'
    last_time.short_description = _('Last time')

    def lookup_allowed(self, key, value):
        return key == 'visit__requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)


class VisitAdmin(admin.ModelAdmin):
    change_form_template = 'request/tracking/visit_change_form.html'
    fieldsets = (
        (_('Visit'), {'fields': ('visitor',)},),
    )
    readonly_fields = ('visitor',)

    date_hierarchy = 'first_time'
    list_display = ('visitor', 'hit_count', 'first_time', 'last_time', 'browser', 'os', 'device')
    list_filter = ('first_time', filters.VisitHitsListFilter)

    def get_queryset(self, request):
        qs = super(VisitAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('requests'),
                         models.Max('requests__time'))
        return qs

    def hit_count(self, obj):
        return obj.requests__count
    hit_count.admin_order_field = 'requests__count'
    hit_count.short_description = _('Hits')

    def last_time(self, obj):
        return obj.requests__time__max
    last_time.admin_order_field = 'requests__time__max'
    last_time.short_description = _('Last time')

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Visit, VisitAdmin)

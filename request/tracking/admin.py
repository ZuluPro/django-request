from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from request.tracking.models import Visitor, Visit


class VisitorAdmin(admin.ModelAdmin):
    change_form_template = 'request/tracking/visitor_change_form.html'
    fieldsets = (
        (_('Visitor'), {'fields': ('key',)},),
    )
    readonly_fields = ('key',)

    date_hierarchy = 'first_time'
    list_display = ('key', 'hits', 'visits', 'first_time', 'last_time')
    list_filter = ('first_time',)

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)


class VisitAdmin(admin.ModelAdmin):
    change_form_template = 'request/tracking/visit_change_form.html'
    fieldsets = (
        (_('Visit'), {'fields': ('visitor',)},),
    )
    readonly_fields = ('visitor',)

    date_hierarchy = 'first_time'
    list_display = ('visitor', 'hits', 'first_time', 'last_time', 'browser', 'os', 'device')
    list_filter = ('first_time',)

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Visit, VisitAdmin)

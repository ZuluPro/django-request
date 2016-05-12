from django.test import TestCase, RequestFactory
from request.tracking.admin import filters
from request.tracking.admin.modeladmins import VisitAdmin, VisitorAdmin
from request.tracking.models import Visit, Visitor


class VisitorHitsListFilter(TestCase):
    def setUp(self):
        self.req_fac = RequestFactory()
        self.req = self.req_fac.get('')
        self.fil = filters.VisitorHitsListFilter(self.req, {}, Visitor, VisitorAdmin)

    def test_lookups(self):
        qs = Visitor.objects.all()
        lookups = self.fil.lookups(self.req, qs)
        self.assertTrue(lookups)

    def test_queryset(self):
        qs = Visitor.objects.all()
        new_qs = self.fil.queryset(self.req, qs)

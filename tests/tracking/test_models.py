from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from request.models import Request
from request.tracking.models import Visit, Visitor


class VisitorModelTest(TestCase):
    def test_str(self):
        visitor = Visitor.objects.create(key='foo')
        visitor.__str__()

    def test_first_time(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        first_time = visitor.first_time
        # 2nd request
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        self.assertEqual(first_time, visitor.first_time)

    def test_last_time(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        last_time = visitor.last_time
        # 2nd request
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        self.assertLess(last_time, visitor.last_time)

    def test_recency(self):
        self.skipTest("Not implemented")

    def test_in_progress(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        self.assertTrue(visitor.in_progress())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertFalse(visitor.in_progress())


class VisitModelTest(TestCase):
    def test_str(self):
        visit = Visit.objects.create(visitor=Visitor.objects.create(key='foo'))
        visit.__str__()

    def test_first_time(self):
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        first_time = visit.first_time
        # 2nd request
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        self.assertEqual(first_time, visit.first_time)

    def test_last_time(self):
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        last_time = visit.last_time
        # 2nd request
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        self.assertLess(last_time, visit.last_time)

    def test_in_progress(self):
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        self.assertTrue(visit.in_progress())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertFalse(visit.in_progress())

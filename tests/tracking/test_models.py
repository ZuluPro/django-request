from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.core.urlresolvers import reverse

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

    def test_ips(self):
        self.client.get('/admin/login/')
        ips = Visitor.objects.first().ips
        self.assertIn('127.0.0.1', ips)
        # Change IP
        Request.objects.update(ip='127.0.0.2')
        self.client.get('/admin/login/')
        ips = Visitor.objects.first().ips
        self.assertIn('127.0.0.1', ips)
        self.assertIn('127.0.0.2', ips)
        self.assertEqual(2, len(ips))

    def test_in_progress(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        self.assertTrue(visitor.in_progress())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertFalse(visitor.in_progress())

    def test_get_absolute_url(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        url = visitor.get_absolute_url()
        wanted_url = reverse('admin:tracking_visitor_change', args=(visitor.id,))
        self.assertEqual(url, wanted_url)

    def test_get_delete_url(self):
        self.client.get('/admin/login/')
        url = Visitor.objects.first().get_delete_url()
        self.assertEqual(url, '/admin/tracking/visitor/1/delete/')


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

    def test_get_absolute_url(self):
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        url = visit.get_absolute_url()
        wanted_url = reverse('admin:tracking_visit_change', args=(visit.id,))
        self.assertEqual(url, wanted_url)

    def test_get_delete_url(self):
        self.client.get('/admin/login/')
        url = Visit.objects.first().get_delete_url()
        self.assertEqual(url, '/admin/tracking/visit/1/delete/')

    def test_ip(self):
        self.client.get('/admin/login/')
        ip = Visit.objects.first().ip
        self.assertEqual(ip, '127.0.0.1')

    def test_user_agent(self):
        self.client.get('/admin/login/')
        user_agent = Visit.objects.first().browser
        self.assertEqual(user_agent, 'Other')

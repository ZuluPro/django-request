from django.test import TestCase
from request.tracking import plugins


class ActiveVisitorTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.ActiveVisitors()
        context = self.plugin.template_context()
        self.assertEqual(0, context['visitors'].count())
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.template_context()
        self.assertEqual(1, context['visitors'].count())

    def test_render(self):
        self.plugin = plugins.ActiveVisitors()
        context = self.plugin.render()
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.render()


class VisitorTrafficInformationTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.VisitorTrafficInformation()
        context = self.plugin.template_context()
        self.assertEqual(0, context['visitors'].count())
        self.assertEqual(0, context['visits'].count())
        self.assertEqual(0, context['requests'].count())
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.template_context()
        self.assertEqual(1, context['visitors'].count())
        self.assertEqual(1, context['visits'].count())
        self.assertEqual(1, context['requests'].count())

    def test_render(self):
        self.plugin = plugins.VisitorTrafficInformation()
        context = self.plugin.render()
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.render()


class LatestVisitsTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.LatestVisits()
        context = self.plugin.template_context()
        self.assertEqual(0, context['visits'].count())
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.template_context()
        self.assertEqual(1, context['visits'].count())

    def test_render(self):
        self.plugin = plugins.LatestVisits()
        context = self.plugin.render()
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.render()

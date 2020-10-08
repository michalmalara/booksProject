from django.test import TestCase, RequestFactory

from books.views import param_replace


class TestParamReplace(TestCase):
    def test_param_replace(self):
        factory = RequestFactory()
        request = factory.get('/?sort_by=title&ascending=true')
        context = {'request': request}
        func_resp = param_replace(context)

        self.assertEquals(func_resp, 'sort_by=title&ascending=true')

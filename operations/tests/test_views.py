from django.test import TestCase
from django.urls import reverse


class TestOperationView(TestCase):
    url_name = "operations:form"

    def setUp(self):
        self.url = reverse(self.url_name)

    def test_correct_response(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200

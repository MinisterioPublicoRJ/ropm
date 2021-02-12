from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class TestOperationView(TestCase):
    url_name = "operations:form"

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.url = reverse(self.url_name)

    def test_correct_response(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(self.url)

        assert resp.status_code == 302

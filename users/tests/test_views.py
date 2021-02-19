from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class TestRevokeUserAccess(TestCase):
    url_name = "users:revoke-access"

    def setUp(self):
        username = "username"
        password = "password"
        self.user = User.objects.create_user(username=username, password=password)
        self.client.force_login(self.user)
        self.url = reverse(self.url_name, kwargs={"username": self.user.username})

        self.p_delete_sessions = mock.patch("users.views.delete_users_all_sessions")
        self.m_delete_sessions = self.p_delete_sessions.start()

    def tearDown(self):
        self.p_delete_sessions.stop()

    def test_revoke_user_access(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 302
        self.m_delete_sessions.assert_called_once_with(self.user)

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(self.url)

        expected_url = f"{reverse('login')}?next={self.url}"
        self.assertRedirects(resp, expected_url, fetch_redirect_response=False)

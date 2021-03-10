from unittest import mock

from django.conf import settings
from django.test import TestCase

from operations.mail import email_login


class TestEmailLogin(TestCase):
    def setUp(self):
        self.smtp_patcher = mock.patch("operations.mail.smtplib.SMTP")
        self.smtp_mock = self.smtp_patcher.start()

    def tearDown(self):
        self.smtp_patcher.stop()

    def test_login(self):
        email_login()

        self.smtp_mock.assert_called_once_with(settings.EMAIL_SMTP_SERVER)

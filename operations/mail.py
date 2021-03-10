import smtplib

from django.conf import settings


def email_login():
    return smtplib.SMTP(settings.EMAIL_SMTP_SERVER)

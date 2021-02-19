from django.contrib.sessions.models import Session
from django.utils import timezone


def delete_users_all_sessions(user):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        if str(user.pk) == session.get_decode().get("_auth_user_id"):
            session.delete()

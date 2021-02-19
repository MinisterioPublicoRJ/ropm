from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse

from users.sessions import delete_users_all_sessions


User = get_user_model()


class RevokeAccessView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, username=self.kwargs.get("username"))
        delete_users_all_sessions(target_user)
        target_user.is_active = False
        target_user.save()

        app_name = User._meta.app_label
        model_name = User._meta.model_name
        redirect_to = reverse(
            f"admin:{app_name}_{model_name}_change",
            args=(target_user.pk,)
        )
        messages.success(
            request,
            f"Acesso do usuário {target_user.username} for revogado com sucesso"
        )
        return HttpResponseRedirect(redirect_to)

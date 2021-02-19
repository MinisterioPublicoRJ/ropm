from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse

from users.sessions import delete_users_all_sessions


User = get_user_model()


class RevokeAccessView(View):
    def get(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, pk=self.kwargs.get("user_pk"))
        delete_users_all_sessions(target_user)

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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("instituicao",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "instituicao")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def reveoke_user_access(self, obj):
        content = ""
        if obj.id:
            url = reverse("users:revoke-access")
            button_name = "Revogar acesso"
            content = format_html(
                f"<button href='{url}'>{button_name}</button>"
            )

        return content


admin.site.register(User, CustomUserAdmin)

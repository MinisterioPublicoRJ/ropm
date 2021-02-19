from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("instituicao",)
    fieldsets = (
        (None, {"fields": ("username", "password", "revoke_user_access")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "instituicao")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = UserAdmin.readonly_fields + ("revoke_user_access",)

    def revoke_user_access(self, obj):
        content = ""
        if obj.id:
            url = reverse("users:revoke-access", args=(obj.username,))
            button_name = "Revogar acesso"
            content = format_html(
                f"<a class='button' href='{url}'>{button_name}</a>"
            )

        return content

    revoke_user_access.short_description = "Acesso"


admin.site.register(User, CustomUserAdmin)

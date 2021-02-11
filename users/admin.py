from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("instituicao",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "instituicao")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, CustomUserAdmin)

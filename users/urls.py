from django.urls import path

from users import views


app_name = "users"
urlpatterns = [
    path("revogar-acesso/<int:user_pk>", views.RevokeAccessView.as_view(), name="revoke-access"),
]

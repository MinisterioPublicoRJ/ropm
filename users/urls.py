from django.urls import path

from users import views


app_name = "users"
urlpatterns = [
    path("revogar-acesso/<str:username>", views.RevokeAccessView.as_view(), name="revoke-access"),
]

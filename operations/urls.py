from django.urls import path

from operations import views

app_name = "operations"
urlpatterns = [
    path("cadastro/", views.OperationReportView.as_view(), name="form"),
    path("lista/", views.OperationListView.as_view(), name="operations-list"),
]

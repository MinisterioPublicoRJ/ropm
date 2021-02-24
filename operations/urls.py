from django.urls import path

from operations import views

app_name = "operations"
urlpatterns = [
    path("cadastro/", views.OperationReportView.as_view(), name="form"),
    path("cadastro/informacoes/resultado", views.OperationInfoResultRegisterView.as_view(), name="form-info-result"),
    path("cadastro/informacoes/operacionais", views.OperationInfoView.as_view(), name="form-info-operation"),
    path("cadastro/informacoes/ocorrencia", views.OperationOcurrenceView.as_view(), name="form-info-ocurrence"),
    path("pagina/inicial", views.InitialPageListView.as_view(), name="initial-page"),
    path("lista/", views.OperationListView.as_view(), name="operations-list"),

]


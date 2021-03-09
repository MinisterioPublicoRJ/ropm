from django.urls import path

from operations import views

app_name = "operations"
urlpatterns = [
    path("cadastro/", views.OperationReportView.as_view(), name="form"),
    path(
        "cadastro/<uuid:form_uuid>",
        views.UpdateOperationReportView.as_view(),
        name="form-update"
    ),
    path(
        "cadastro/informacoes/adpf-635/<uuid:form_uuid>",
        views.OperationADPF635View.as_view(),
        name="form-info-adpf-635"
    ),
    path(
        "cadastro/informacoes/operacionais/parte-1/<uuid:form_uuid>",
        views.OperationInfoPageOneView.as_view(),
        name="form-info-operation-page-one"
    ),
    path(
        "cadastro/informacoes/operacionais/parte-2/<uuid:form_uuid>",
        views.OperationInfoPageTwoView.as_view(),
        name="form-info-operation-page-two"
    ),
    path(
        "cadastro/informacoes/resultado/<uuid:form_uuid>",
        views.OperationInfoResultRegisterView.as_view(),
        name="form-info-result"
    ),
    path(
        "cadastro/informacoes/ocorrencia/parte-1/<uuid:form_uuid>",
        views.OperationOcurrencePageOneView.as_view(),
        name="form-info-ocurrence-page-one"
    ),
    path(
        "cadastro/completo/<uuid:form_uuid>",
        views.FormCompleteView.as_view(),
        name="form-complete"
    ),
    path(
        "cadastro/informacoes/ocorrencia/parte-2/<uuid:form_uuid>",
        views.OperationOcurrencePageTwoView.as_view(),
        name="form-info-ocurrence-page-two"
    ),
    path("lista/", views.OperationListView.as_view(), name="operations-list"),
    path("painel/", views.PanelListView.as_view(), name="operations-panel"),
]

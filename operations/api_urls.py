from django.urls import path

from operations import api_views


single_actions = {
    "get": "retrieve",
    "put": "update",
}


app_name = "operations_api"
urlpatterns = [
    path(
        "cria-informacoes-gerais/<uuid:form_uuid>",
        api_views.GeneralInfoViewSet.as_view(single_actions),
        name="create-general-info"
    ),
    path(
        "cria-informacoes-adpf635/<uuid:form_uuid>",
        api_views.OperationInfoADPF635ViewSet.as_view(single_actions),
        name="create-adpf635l-info"
    ),
    path(
        "cria-informacoes-operacionais-parte-1/<uuid:form_uuid>",
        api_views.OperationalInfoOneViewSet.as_view(single_actions),
        name="create-operational-info-1"
    ),
    path(
        "cria-informacoes-operacionais-parte-2/<uuid:form_uuid>",
        api_views.OperationalInfoTwoViewSet.as_view(single_actions),
        name="create-operational-info-2"
    ),
    path(
        "cria-informacoes-resultado/<uuid:form_uuid>",
        api_views.ResultInfoViewSet.as_view(single_actions),
        name="create-result-info"
    ),
    path(
        "cria-informacoes-ocorrencia-parte-1/<uuid:form_uuid>",
        api_views.OcurrenceInfoOneViewSet.as_view(single_actions),
        name="create-ocurrence-info-1"
    ),
    path(
        "cria-informacoes-ocorrencia-parte-2/<uuid:form_uuid>",
        api_views.OcurrenceInfoTwoViewSet.as_view(single_actions),
        name="create-ocurrence-info-2"
    ),
    path(
        "cria-informacoes-observacoes-gerais/<uuid:form_uuid>",
        api_views.GeneralObservationViewSet.as_view(single_actions),
        name="create-general-observation"
    ),
]

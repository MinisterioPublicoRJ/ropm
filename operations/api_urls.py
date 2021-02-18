from django.urls import path

from operations import api_views


single_actions = {
    "get": "retrieve",
    "put": "update",
    "post": "create",
}


app_name = "operations_api"
urlpatterns = [
    path(
        "cria-informacoes-gerais/<uuid:form_uuid>",
        api_views.GeneralInfoViewSet.as_view(single_actions),
        name="create-general-info"
    ),
    path(
        "cria-informacoes-operacionais/<uuid:form_uuid>",
        api_views.OperationalInfoViewSet.as_view(single_actions),
        name="create-operational-info"
    ),
]

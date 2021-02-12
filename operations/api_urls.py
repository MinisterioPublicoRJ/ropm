from django.urls import path

from operations import api_views


app_name = "operations_api"
urlpatterns = [
    path(
        "cria-informacoes-gerais/<uuid:form_uuid>",
        api_views.CreateGeneralInfo.as_view(),
        name="create-general-info"
    ),
]

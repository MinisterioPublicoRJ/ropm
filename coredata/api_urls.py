from django.urls import path

from coredata import api_views


app_name = "coredata"
urlpatterns = [
    path("municipios-rj", api_views.MunicipiosView.as_view(), name="municipios-list"),
    path("bairros-rj/<str:nm_mun>", api_views.BairrosView.as_view(), name="bairros-list"),
    path("batalhoes-rj/<str:nm_mun>", api_views.BatalhaoView.as_view(), name="batalhoes-list"),
    path("delegacias-rj/<int:cod_mun>", api_views.DelegaciaView.as_view(), name="delegacias-list"),
]

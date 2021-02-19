from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from coredata.models import (
    Bairro,
    Batalhao,
    Delegacia,
    Municipio,
)
from coredata.serializers import (
    BairroSerializer,
    BatalhaoSerializer,
    DelegaciaSerializer,
    MunicipioSerializer
)


class MunicipiosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Municipio.objects.all().order_by("nm_mun")
    serializer_class = MunicipioSerializer


class BairrosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BairroSerializer
    lookup_url_kwarg = "cod_mun"

    def get_queryset(self):
        cod_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Bairro.objects.filter(
            cod_mun__cod_6_dig=cod_mun
        ).order_by("bairro")


class BatalhaoView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BatalhaoSerializer
    lookup_url_kwarg = "cod_mun"

    def get_queryset(self):
        cod_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Batalhao.objects.filter(
            codigo_mun__cod_6_dig=cod_mun
        ).order_by("bpm").distinct("bpm")


class DelegaciaView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DelegaciaSerializer
    lookup_url_kwarg = "cod_mun"

    def get_queryset(self):
        cod_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Delegacia.objects.filter(
            cod_mun__cod_6_dig=cod_mun
        ).order_by("nome").distinct("nome")

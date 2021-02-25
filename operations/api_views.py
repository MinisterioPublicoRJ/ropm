from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from operations.models import (
    InformacaoGeralOperacao,
    InformacaoOperacionalOperacao,
    Operacao,
)
from operations.serializers import (
    InformacaoGeralOperacaoSerializer,
    InformacaoOperacionalOperacaoSerializer,
)


class GeneralInfoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InformacaoGeralOperacaoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "operacao__identificador"

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return InformacaoGeralOperacao.objects.filter(
            operacao__usuario=user,
            operacao__identificador=identificador
        )

    def get_or_create_operation(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        objs = Operacao.objects.filter(identificador=identificador)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=identificador, usuario=user)

        return obj

    def perform_create(self, serializer):
        operacao = self.get_or_create_operation()
        serializer.instance = InformacaoGeralOperacao.objects.get_or_none(operacao)
        serializer.save(operacao=operacao)


class OperationalInfoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InformacaoOperacionalOperacaoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "operacao__identificador"

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(operacao=self.get_operation())

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return InformacaoOperacionalOperacao.objects.filter(
            operacao__usuario=user,
            operacao__identificador=identificador
        )

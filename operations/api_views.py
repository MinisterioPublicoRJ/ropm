from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        return InformacaoGeralOperacao.objects.filter(
            operacao__usuario=user,
            operacao__identificador=form_uuid
        )

    def get_or_create_operation(self, user, id_):
        objs = Operacao.objects.filter(identificador=id_)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=id_, usuario=user)

        return obj

    def create(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        user = self.request.user
        operacao = self.get_or_create_operation(user, form_uuid)
        ser = self.get_serializer_class()(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(operacao=operacao)
        return Response()


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
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        return InformacaoOperacionalOperacao.objects.filter(
            operacao__usuario=user,
            operacao__identificador=form_uuid
        )

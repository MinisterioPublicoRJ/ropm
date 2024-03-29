from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from operations.mixins import AllowPUTAsCreateMixin
from operations.models import Operacao
from operations.serializers import (
    GeneralObservationSerializer,
    InfoADPF635Serializer,
    InfoGeraisOperacaoSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoResultadosOperacaoSerializer,
    InfoOcorrenciaOneSerializer,
    InfoOcorrenciaTwoSerializer,
)


class GeneralInfoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoGeraisOperacaoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 2

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def get_operation(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        objs = Operacao.objects.filter(identificador=identificador)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=identificador, usuario=user)

        return obj


class OperationInfoADPF635ViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoADPF635Serializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 3

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def get_operation(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        objs = Operacao.objects.filter(identificador=identificador)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=identificador, usuario=user)

        return obj


class OperationalInfoOneViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOperacionaisOperacaoOneSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 4

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class OperationalInfoTwoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOperacionaisOperacaoTwoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 5

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class ResultInfoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoResultadosOperacaoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 6

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class OcurrenceInfoOneViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOcorrenciaOneSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 7

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class OcurrenceInfoTwoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOcorrenciaTwoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 8

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class GeneralObservationViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneralObservationSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 9

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

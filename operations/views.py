import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.urls import reverse

from coredata.models import Bairro, Batalhao, Municipio
from operations.models import Operacao
from operations.serializers import (
    GeneralObservationSerializer,
    InfoADPF635Serializer,
    InfoGeraisOperacaoSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoOcorrenciaOneSerializer,
    InfoOcorrenciaTwoSerializer,
    InfoResultadosOperacaoSerializer,
)


URL_SECTION_MAPPER = {
    1: "operations:form-update",
    2: "operations:form-info-adpf-635",
    3: "operations:form-info-operation-page-one",
    4: "operations:form-info-operation-page-two",
    5: "operations:form-info-result",
    6: "operations:form-info-ocurrence-page-one",
    7: "operations:form-info-ocurrence-page-two",
    8: "operations:form-observacoes-gerais",
    9: "operations:form-complete",
}


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        context["municipios"] = Municipio.objects.get_ordered_values()
        nm_first_city = context["municipios"][0]["nm_mun"]
        context["bairros"] = Bairro.objects.get_ordered_for_municipio(nm_first_city)
        context["batalhoes"] = Batalhao.objects.get_ordered_for_municipio(nm_first_city)
        context["operacao_data"] = dict()
        return context


class OperationViewMixin:
    def get_serialized_data(self, operacao):
        return self.serializer_class(operacao).data

    def dispatch(self, request, *args, **kwargs):
        # TODO: Refatorar essa lógica
        self.form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.operacao = self.get_operation(self.request.user, self.form_uuid)

        if  (
            self.operacao.houve_ocorrencia_operacao is False and
            self.section_number in settings.SKIPPABLE_SECTIONS
        ):
            self.operacao.update_section(OperationGeneralObservation.section_number)
            reverse_url = reverse(
                "operations:form-observacoes-gerais",
                kwargs={"form_uuid": self.form_uuid}
            )
            if request.path != reverse_url:
                return redirect(reverse_url)

        if self.section_number > self.operacao.secao_atual:
            secao_atual_url = URL_SECTION_MAPPER[self.operacao.secao_atual]
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )

        handler = super().dispatch(request, *args, **kwargs)
        return handler

    def get_operation(self, usuario, form_uuid):
        return get_object_or_404(
            Operacao,
            identificador=form_uuid,
            usuario=usuario
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = self.form_uuid
        context["operacao_info"] = self.get_serialized_data(self.operacao)
        return context


# TODO: add tests
class UpdateOperationReportView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoGeraisOperacaoSerializer

    section_number = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["municipios"] = Municipio.objects.get_ordered_values()
        context["bairros"] = Bairro.objects.get_ordered_for_municipio(
            context["operacao_info"]["municipio"]
        )
        context["batalhoes"] = Batalhao.objects.get_ordered_for_municipio(
            context["operacao_info"]["municipio"]
        )
        return context


class OperationADPF635View(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_ADPF_635.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoADPF635Serializer

    section_number = 2


# TODO: add tests
class OperationInfoPageOneView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoOneSerializer

    section_number = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postos_comandante"] = Operacao.POSTO_COMANDANTE
        return context


class OperationInfoPageTwoView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoTwoSerializer

    section_number = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipos_operacoes"] = Operacao.TIPO_OPERACAO
        context["tipos_acoes_repressivas"] = Operacao.TIPO_ACAO_REPRESSIVA
        return context


class OperationInfoResultRegisterView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_result_info.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoResultadosOperacaoSerializer

    section_number = 5


class OperationOcurrencePageOneView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOcorrenciaOneSerializer

    section_number = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postos_comandante"] = Operacao.POSTO_COMANDANTE
        return context


class OperationOcurrencePageTwoView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOcorrenciaTwoSerializer

    section_number = 7


class OperationGeneralObservation(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/general_observations.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = GeneralObservationSerializer

    section_number = 8


class FormCompleteView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_complete.html"
    lookup_url_kwarg = "form_uuid"

    section_number = 8

    def get_serialized_data(self, operacao):
        return {}

    def dispatch(self, request, *args, **kwargs):
        # TODO: Refatorar essa lógica
        handler = super().dispatch(request, *args, **kwargs)
        if request.user.is_anonymous:
            return handler

        self.form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.operacao = self.get_operation(self.request.user, self.form_uuid)

        secao_atual_url = URL_SECTION_MAPPER.get(self.operacao.secao_atual)
        if self.operacao.secao_atual == Operacao.n_sections + 1:
            return handler
        if (
            self.operacao.secao_atual == Operacao.n_sections
            and self.operacao.houve_ocorrencia_operacao is True
        ):
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )
        if (
            self.operacao.secao_atual == Operacao.n_sections
            and self.operacao.houve_ocorrencia_operacao is False
        ):
            return handler
        if (
            self.operacao.secao_atual in settings.SKIPPABLE_SECTIONS
            and self.operacao.houve_ocorrencia_operacao is False
        ):
            return handler
        else:
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )

    def get_operation(self, usuario, form_uuid):
        return get_object_or_404(
            Operacao,
            identificador=form_uuid,
            usuario=usuario
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        operacao = self.get_operation(self.request.user, form_uuid)
        context["form_uuid"] = form_uuid
        context["operacao_info"] = self.get_serialized_data(operacao)
        return context


class OperationListView(LoginRequiredMixin, ListView):
    template_name = "operations/operations_list_template.html"
    paginate_by = settings.OPERATIONS_PER_PAGE

    def get_queryset(self):
        return Operacao.objects.filter(usuario=self.request.user).order_by("-criado_em")


class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"


class PanelListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/panel_template.html"

import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from coredata.models import Bairro, Batalhao, Municipio
from operations.models import Operacao
from operations.serializers import (
    InfoGeraisOperacaoSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoResultadosOperacaoSerializer,
)


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        context["form_uuid"] = form_uuid
        operacao_info = get_object_or_404(
            Operacao,
            identificador=form_uuid,
            usuario=self.request.user
        )
        operacao_info = self.serializer_class(operacao_info).data
        context["operacao_info"] = operacao_info
        return context


# TODO: add tests
class UpdateOperationReportView(OperationViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoGeraisOperacaoSerializer

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


# TODO: add tests
class OperationInfoPageOneView(OperationViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoOneSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postos_comandante"] = Operacao.POSTO_COMANDANTE
        return context


class OperationInfoPageTwoView(OperationViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoTwoSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipos_operacoes"] = Operacao.TIPO_OPERACAO
        context["tipos_acoes_repressivas"] = Operacao.TIPO_ACAO_REPRESSIVA
        return context


class OperationInfoResultRegisterView(OperationViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_result_info.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoResultadosOperacaoSerializer


class OperationOcurrencePageOneView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_one.html"


class OperationOcurrencePageTwoView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_two.html"


class OperationListView(LoginRequiredMixin, ListView):
    template_name = "operations/operations_list_template.html"
    paginate_by = settings.OPERATIONS_PER_PAGE

    def get_queryset(self):
        return Operacao.objects.filter(usuario=self.request.user)


class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"


class PanelListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/panel_template.html"

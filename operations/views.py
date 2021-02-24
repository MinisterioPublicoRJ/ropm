import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from coredata.models import Bairro, Batalhao, Municipio


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        context["municipios"] = Municipio.objects.get_ordered_values()
        nm_first_city = context["municipios"][0]["nm_mun"]
        context["bairros"] = Bairro.objects.get_ordered_for_municipio(nm_first_city)
        context["batalhoes"] = Batalhao.objects.get_ordered_for_municipio(nm_first_city)
        return context


class OperationInfoResultRegisterView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_result_info.html"


class OperationInfoView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation.html"


class OperationOcurrenceView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence.html"


class OperationListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/operations_list_template.html"

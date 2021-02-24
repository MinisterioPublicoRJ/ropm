import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        return context

# Classes que renderizam as páginas dos templates form
class OperationInfoResultRegisterView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_result_info.html"

class OperationInfoView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation.html"

class OperationOcurrenceView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence.html"

# Classes que renderizam as páginas dos do app
class OperationListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/operations_list_template.html"

class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"

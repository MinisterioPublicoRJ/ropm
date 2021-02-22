import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        return context

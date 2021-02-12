from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

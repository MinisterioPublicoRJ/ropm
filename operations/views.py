from django.views.generic import TemplateView


class OperationReportView(TemplateView):
    template_name = "operations/form_template.html"

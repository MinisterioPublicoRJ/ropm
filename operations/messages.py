from django.template.loader import get_template

from operations.serializers import OperacaoEmailSerializer


class Mensagem:
    template_name = "operations/email_template.html"

    def __init__(self, operacao):
        self.operacao = operacao

    @property
    def context(self):
        ser = OperacaoEmailSerializer(instance=self.operacao)
        return ser.data

    def render(self):
        template = get_template(self.template_name)
        return template.render(context=self.context)

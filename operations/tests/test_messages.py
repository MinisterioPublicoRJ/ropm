from django.test import TestCase
from model_bakery import baker

from operations.messages import Mensagem
from operations.models import Operacao


class TestMensagem(TestCase):
    def setUp(self):
        self.operacao = baker.make(Operacao, _fill_optional=True)
        self.message = Mensagem(operacao=self.operacao)

    def test_get_message_context(self):
        context = self.message.context
        expected_context = {"bairro": self.operacao.bairro}

        assert context == expected_context

    def test_render_message(self):
        rendered_messaege = self.message.render()

        assert "<html>" in rendered_messaege
        assert "</html>" in rendered_messaege
        assert self.operacao.bairro in rendered_messaege

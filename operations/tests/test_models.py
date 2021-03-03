import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker

from operations.models import Operacao


User = get_user_model()


class TestOperationFlow(TestCase):
    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.form_uuid = uuid.uuid4()
        self.operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
        )

    def test_operacao_starts_at_secao_1(self):
        assert self.operacao.secao_atual == 1

    def test_update_section(self):
        new_section = 2
        section = self.operacao.update_section(new_section)

        self.operacao.refresh_from_db()
        assert section == new_section
        assert self.operacao.secao_atual == new_section

    def test_go_to_next_section(self):
        new_section = 3
        self.operacao.houve_ocorrencia_operacao = True
        self.operacao.update_section(new_section)

        self.operacao.refresh_from_db()
        assert self.operacao.secao_atual == new_section

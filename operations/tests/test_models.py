import uuid

from django.test import TestCase
from model_bakery import baker

from operations.models import Operacao


class TestOperationFlow(TestCase):
    def setUp(self):
        self.form_uuid = uuid.uuid4()
        self.operacao = baker.make(
            Operacao,
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


class TestOperationMakeComplete(TestCase):
    def setUp(self):
        self.form_uuid = uuid.uuid4()

    def test_operacao_starts_with_status_incomplete(self):
        operacao = baker.make(
            Operacao,
            identificador=self.form_uuid,
        )

        assert operacao.situacao == "incompleto"

    def test_make_complete(self):
        operacao = baker.make(
            Operacao,
            identificador=self.form_uuid,
            houve_ocorrencia_operacao=True
        )
        operacao.make_complete()

        operacao.refresh_from_db()
        assert operacao.completo
        assert operacao.situacao == "completo com ocorrencia"

    def test_make_complete_with_status_not_all_sections_filled(self):
        operacao = baker.make(
            Operacao,
            identificador=self.form_uuid,
            houve_ocorrencia_operacao=False
        )
        operacao.make_complete()

        operacao.refresh_from_db()
        assert operacao.completo
        assert operacao.situacao == "completo sem ocorrencia"

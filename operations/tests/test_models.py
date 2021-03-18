import uuid
from unittest import mock

import pytest
from django.conf import settings
from django.test import TestCase, override_settings
from model_bakery import baker

from operations.exceptions import OperationNotCompleteException
from operations.models import Operacao


class TestOperationModel(TestCase):
    def setUp(self):
        self.operacao = baker.make(Operacao)

    def test_get_admin_url(self):
        admin_url = self.operacao.get_admin_url
        expected = f"{settings.SITE_URL}/admin/operations/operacao/{self.operacao.id}/change/"

        assert admin_url == expected


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

        self.p_notify = mock.patch.object(Operacao, "notify_completion")
        self.m_notify = self.p_notify.start()

    def tearDown(self):
        self.p_notify.stop()

    def test_operacao_starts_with_status_incomplete(self):
        operacao = baker.make(
            Operacao,
            identificador=self.form_uuid,
        )

        assert operacao.situacao == "incompleto"

    def test_make_complete(self):
        operacao = baker.make(
            Operacao,
            completo=False,
            identificador=self.form_uuid,
            houve_ocorrencia_operacao=True
        )
        operacao.make_complete()

        operacao.refresh_from_db()
        assert operacao.completo
        assert operacao.situacao == "completo com ocorrencia"
        self.m_notify.assert_called_once_with()

    def test_make_complete_with_status_not_all_sections_filled(self):
        operacao = baker.make(
            Operacao,
            completo=False,
            identificador=self.form_uuid,
            houve_ocorrencia_operacao=False
        )
        operacao.make_complete()

        operacao.refresh_from_db()
        assert operacao.completo
        assert operacao.situacao == "completo sem ocorrencia"
        self.m_notify.assert_called_once_with()

    def test_only_notify_when_complete_for_the_first_time(self):
        operacao = baker.make(
            Operacao,
            completo=True,
            identificador=self.form_uuid,
            houve_ocorrencia_operacao=False
        )
        operacao.make_complete()

        operacao.refresh_from_db()
        assert operacao.completo
        assert operacao.situacao == "completo sem ocorrencia"
        self.m_notify.assert_not_called()


class TestNotifyOperationComplete(TestCase):
    def setUp(self):
        self.identificador = uuid.uuid4()
        self.operacao_completa = baker.make(
            Operacao,
            completo=True,
            identificador=self.identificador
        )
        self.operacao_incompleta = baker.make(
            Operacao,
            completo=False,
            identificador=uuid.uuid4()
        )
        self.p_notifica_por_email = mock.patch("operations.models.notifica_por_email")
        self.m_noifica_por_email = self.p_notifica_por_email.start()

    def tearDown(self):
        self.p_notifica_por_email.stop()

    @override_settings(DEBUG=False)
    def test_notify_when_complete(self):
        self.operacao_completa.notify_completion()

        self.m_noifica_por_email.assert_called_once_with(self.operacao_completa)

    def test_raise_exception_when_not_complete(self):
        with pytest.raises(OperationNotCompleteException):
            self.operacao_incompleta.notify_completion()

    @override_settings(DEBUG=True)
    def test_donot_notfy_when_in_debug_mode(self):
        self.operacao_completa.notify_completion()

        self.m_noifica_por_email.assert_not_called()

import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from operations.models import (
    InformacaoGeralOperacao,
    InformacaoOperacionalOperacao,
    Operacao,
)


User = get_user_model()


class TestSendInformacaoGeralOperacao(TestCase):
    url_name = "api-operations:create-general-info"

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})

        self.form_data = {
            "data": "2021-02-12",
            "hora": "12:00:00",
            "localidade": "Rua A",
            "bairro": "Bairro B",
            "municipio": "Rio de Janeiro",
            "endereco_referencia": "Primeira rua",
            "coordenadas_geo": "-12.9999,45.4555",
            "batalhao_responsavel": "X BPM",
        }

    def test_save_database_info(self):
        resp = self.client.post(self.url, data=self.form_data)

        assert resp.status_code == 201
        op = Operacao.objects.get(identificador=self.form_uuid)
        InformacaoGeralOperacao.objects.get(operacao=op)
        assert op.usuario == self.user
        assert not op.editado

    def test_retrieve_saved_info(self):
        operacao = baker.make(Operacao, usuario=self.user, identificador=self.form_uuid)
        op_general_info = baker.make(InformacaoGeralOperacao, operacao=operacao)

        resp = self.client.get(self.url)
        data = resp.data

        assert resp.status_code == 200
        assert data["data"] == op_general_info.data.strftime("%Y-%m-%d")
        assert data["hora"] == op_general_info.hora.strftime("%H:%M:%S")
        assert data["localidade"] == op_general_info.localidade
        assert data["bairro"] == op_general_info.bairro
        assert data["municipio"] == op_general_info.municipio
        assert data["endereco_referencia"] == op_general_info.endereco_referencia
        assert data["batalhao_responsavel"] == op_general_info.batalhao_responsavel

    def test_update_some_fields(self):
        operacao = baker.make(Operacao, usuario=self.user, identificador=self.form_uuid)
        op_general_info = baker.make(
            InformacaoGeralOperacao,
            operacao=operacao
        )

        new_info = "Novo Bairro"
        self.form_data["bairro"] = new_info
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        op_general_info.refresh_from_db()
        assert InformacaoGeralOperacao.objects.count() == 1
        assert resp.status_code == 200
        assert op_general_info.bairro == new_info

    def test_another_user_tries_to_update_info(self):
        baker.make(Operacao, usuario=self.user, identificador=self.form_uuid)

        self.client.logout()
        self.username = "another-username"
        self.pwd = "pwd1234"

        user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(user)

        self.form_data["bairro"] = "novo bairro"
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        assert resp.status_code == 404

    def test_404_for_object_doesnt_exists(self):
        baker.make(Operacao, usuario=self.user)

        resp = self.client.get(self.url)

        assert resp.status_code == 404

    def test_user_cannot_delete_info(self):
        resp = self.client.delete(self.url)

        assert resp.status_code == 405

    def test_login_required(self):
        self.client.logout()
        resp = self.client.post(self.url)

        assert resp.status_code == 403

    def test_another_user_tries_to_retrive_info(self):
        self.username = "another-username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        resp = self.client.get(self.url)

        assert resp.status_code == 404


class TestSendInformacaoOperacionalOperacao(TestCase):
    url_name = "api-operations:create-operational-info"

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})

        self.operacao = baker.make(Operacao, usuario=self.user, identificador=self.form_uuid)

        self.form_data = {
            "unidade_responsavel": "Unidade A",
            "apoio_outras_unidades": False,
            "nome_comandante": "Nome Comandante",
            "rg_pm_comandante": "123456",
            "posto_comandante": "Maj",
            "tipo_operacao": "Pl",
            "tipo_de_acao_repressiva": "AREP II",
            "objetivo_operacao": "Objetivo A",
            "numero_policiais_mobilizados": 10,
        }

    def test_save_database_info(self):
        resp = self.client.post(self.url, data=self.form_data)

        assert resp.status_code == 201
        op = Operacao.objects.get(identificador=self.form_uuid)
        InformacaoOperacionalOperacao.objects.get(operacao=op)

    def test_retrieve_saved_info(self):
        op_operational_info = baker.make(InformacaoOperacionalOperacao, operacao=self.operacao)

        resp = self.client.get(self.url)
        data = resp.data

        assert resp.status_code == 200
        assert data["unidade_responsavel"] == op_operational_info.unidade_responsavel
        assert data["apoio_outras_unidades"] == op_operational_info.apoio_outras_unidades
        assert data["nome_comandante"] == op_operational_info.nome_comandante
        assert data["rg_pm_comandante"] == op_operational_info.rg_pm_comandante
        assert data["posto_comandante"] == op_operational_info.posto_comandante
        assert data["tipo_operacao"] == op_operational_info.tipo_operacao
        assert data["tipo_de_acao_repressiva"] == op_operational_info.tipo_de_acao_repressiva
        assert data["objetivo_operacao"] == op_operational_info.objetivo_operacao
        assert data["numero_policiais_mobilizados"] == op_operational_info.numero_policiais_mobilizados

    def test_update_some_fields(self):
        operacao = Operacao.objects.get(identificador=self.form_uuid)
        op_operational_info = baker.make(
            InformacaoOperacionalOperacao,
            operacao=operacao
        )

        new_info = "891011"
        self.form_data["rg_pm_comandante"] = new_info
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        op_operational_info.refresh_from_db()
        assert resp.status_code == 200
        assert InformacaoOperacionalOperacao.objects.count() == 1
        op_operational_info = InformacaoOperacionalOperacao.objects.get(
            operacao=operacao
        )
        assert op_operational_info.rg_pm_comandante == new_info

    def test_user_cannot_delete_info(self):
        resp = self.client.delete(self.url)

        assert resp.status_code == 405

    def test_another_user_tries_to_update_info(self):
        self.client.logout()
        self.username = "another-username"
        self.pwd = "pwd1234"

        user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(user)

        self.form_data["bairro"] = "novo bairro"
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        assert resp.status_code == 404

    def test_404_for_object_doesnt_exists(self):
        baker.make(Operacao, usuario=self.user)

        resp = self.client.get(self.url)

        assert resp.status_code == 404

    def test_login_required(self):
        self.client.logout()
        resp = self.client.post(self.url)

        assert resp.status_code == 403

    def test_another_user_tries_to_retrive_info(self):
        self.username = "another-username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        resp = self.client.get(self.url)

        assert resp.status_code == 404

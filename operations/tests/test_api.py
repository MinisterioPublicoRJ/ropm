import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from operations.models import Operacao
from operations.model_recipes import (
    op_recipe_with_occurence,
    op_recipe_without_occurence,
)

from operations.api_views import (
    OcurrenceInfoOneViewSet,
    OcurrenceInfoTwoViewSet,
    OperationalInfoOneViewSet,
    OperationalInfoTwoViewSet,
    ResultInfoViewSet,
)
from operations.serializers import (
    InfoOcorrenciaOneSerializer,
    InfoOcorrenciaTwoSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoResultadosOperacaoSerializer,
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
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        assert resp.status_code == 200
        operacao = Operacao.objects.get(identificador=self.form_uuid)
        assert operacao.usuario == self.user

        data = resp.data
        assert data["data"] == operacao.data.strftime("%Y-%m-%d")
        assert data["hora"] == operacao.hora.strftime("%H:%M:%S")
        assert data["localidade"] == operacao.localidade
        assert data["bairro"] == operacao.bairro
        assert data["municipio"] == operacao.municipio
        assert data["endereco_referencia"] == operacao.endereco_referencia
        assert data["batalhao_responsavel"] == operacao.batalhao_responsavel

    def test_retrieve_saved_info(self):
        operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
            _fill_optional=True
        )

        resp = self.client.get(self.url)
        data = resp.data

        assert resp.status_code == 200
        assert data["data"] == operacao.data.strftime("%Y-%m-%d")
        assert data["hora"] == operacao.hora.strftime("%H:%M:%S")
        assert data["localidade"] == operacao.localidade
        assert data["bairro"] == operacao.bairro
        assert data["municipio"] == operacao.municipio
        assert data["endereco_referencia"] == operacao.endereco_referencia
        assert data["batalhao_responsavel"] == operacao.batalhao_responsavel

    def test_update_some_fields(self):
        operacao = baker.make(Operacao, usuario=self.user, identificador=self.form_uuid)

        new_info = "Novo Bairro"
        self.form_data["bairro"] = new_info
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        operacao.refresh_from_db()
        assert Operacao.objects.count() == 1
        assert resp.status_code == 200
        assert operacao.bairro == new_info

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
    url_name = "api-operations:create-operational-info-1"

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})

        self.operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
            _fill_optional=True
        )

        self.form_data = {
            "unidade_responsavel": "Unidade A",
            "unidade_apoiadora": "Unidade X",
            "nome_comandante_operacao": "Nome Comandante",
            "rg_pm_comandante_operacao": "123456",
            "posto_comandante_operacao": "Maj",
        }

    def test_save_database_info(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        assert resp.status_code == 200
        operacao = Operacao.objects.get(identificador=self.form_uuid)

        data = resp.data
        assert data["unidade_responsavel"] == operacao.unidade_responsavel
        assert data["unidade_apoiadora"] == operacao.unidade_apoiadora
        assert data["nome_comandante_operacao"] == operacao.nome_comandante_operacao
        assert data["rg_pm_comandante_operacao"] == operacao.rg_pm_comandante_operacao
        assert data["posto_comandante_operacao"] == operacao.posto_comandante_operacao

    def test_retrieve_saved_info(self):
        resp = self.client.get(self.url)
        data = resp.data

        assert resp.status_code == 200
        assert data["unidade_responsavel"] == self.operacao.unidade_responsavel
        assert data["unidade_apoiadora"] == self.operacao.unidade_apoiadora
        assert data["nome_comandante_operacao"] == self.operacao.nome_comandante_operacao
        assert data["rg_pm_comandante_operacao"] == self.operacao.rg_pm_comandante_operacao
        assert data["posto_comandante_operacao"] == self.operacao.posto_comandante_operacao

    def test_update_some_fields(self):
        operacao = Operacao.objects.get(identificador=self.form_uuid)

        new_info = "891011"
        self.form_data["rg_pm_comandante_operacao"] = new_info
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        operacao.refresh_from_db()
        assert resp.status_code == 200
        assert Operacao.objects.count() == 1
        assert operacao.rg_pm_comandante_operacao == new_info

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

        url = reverse(self.url_name, kwargs={"form_uuid": uuid.uuid4()})
        resp = self.client.get(url)

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


class TestOperationSectionFlowMixin:
    url_name = None
    view_class = None
    serializer_class = None
    expected_section = None

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
        )
        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})
        self.op_recipe_obj = op_recipe_with_occurence.prepare()

        self.form_data = self.serializer_class(self.op_recipe_obj).data


class TestOperationUpdateToSecondSection(TestOperationSectionFlowMixin, TestCase):
    url_name = "operations_api:create-operational-info-1"
    view_class = OperationalInfoOneViewSet
    serializer_class = InfoOperacionaisOperacaoOneSerializer
    expected_section = 3

    def test_update_section_when_saving_data(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )
        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section


class TestOperationUpdateToThirdSection(TestOperationSectionFlowMixin, TestCase):
    url_name = "operations_api:create-operational-info-2"
    view_class = OperationalInfoTwoViewSet
    serializer_class = InfoOperacionaisOperacaoTwoSerializer
    expected_section = 4

    def test_update_section_when_saving_data(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )
        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section


class TestOperationUpdateToFourthSection(TestOperationSectionFlowMixin, TestCase):
    url_name = "operations_api:create-result-info"
    view_class = ResultInfoViewSet
    serializer_class = InfoResultadosOperacaoSerializer
    expected_section = 5

    def test_update_section_when_saving_data(self):
        self.form_data["houve_ocorrencia_operacao"] = True
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )
        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section


class TestOperationUpdateToFifthSection(TestOperationSectionFlowMixin, TestCase):
    url_name = "operations_api:create-ocurrence-info-1"
    view_class = OcurrenceInfoOneViewSet
    serializer_class = InfoOcorrenciaOneSerializer
    expected_section = 6

    def test_update_section_when_saving_data(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )
        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section


class TestOperationUpdateToSixthSection(TestOperationSectionFlowMixin, TestCase):
    url_name = "operations_api:create-ocurrence-info-2"
    view_class = OcurrenceInfoTwoViewSet
    serializer_class = InfoOcorrenciaTwoSerializer
    expected_section = 7

    def test_update_section_when_saving_data(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )
        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section


class TestOperationFlowSkipLastSections(TestCase):
    """
        Quando o campo 'houve_ocorrencia_operacao' for False, as seções 5 e 6
        são ignoradas
    """
    url_name = "operations_api:create-result-info"
    view_class = ResultInfoViewSet
    serializer_class = InfoResultadosOperacaoSerializer
    expected_section = 5

    def setUp(self):
        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
        )
        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})
        self.op_recipe_obj = op_recipe_without_occurence.prepare()
        self.form_data = self.serializer_class(self.op_recipe_obj).data
        self.form_data["houve_ocorrencia_operacao"] = False

    def test_skip_to_last_section(self):
        resp = self.client.put(
            self.url,
            data=self.form_data,
            content_type="application/json",
        )

        self.operacao.refresh_from_db()
        assert resp.status_code == 200
        assert self.operacao.secao_atual == self.expected_section

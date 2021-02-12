import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from operations.models import InformacaoGeralOperacao, Operacao


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

        assert resp.status_code == 200
        op = Operacao.objects.get(identificador=self.form_uuid)
        op_general_info = InformacaoGeralOperacao.objects.get(operacao=op)
        assert op.usuario == self.user
        assert not op.editado

    def test_login_required(self):
        self.client.logout()
        resp = self.client.post(self.url)

        assert resp.status_code == 403

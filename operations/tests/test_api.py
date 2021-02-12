import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from operations.models import Operacao


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

    def test_save_database_info(self):
        resp = self.client.post(self.url)

        op = Operacao.objects.get(identificador=self.form_uuid)
        assert resp.status_code == 200
        assert op.usuario == self.user
        assert not op.editado

    def test_login_required(self):
        self.client.logout()
        resp = self.client.post(self.url)

        assert resp.status_code == 403

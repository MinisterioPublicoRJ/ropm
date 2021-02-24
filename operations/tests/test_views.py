from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from coredata.models import Bairro, Batalhao, Municipio

User = get_user_model()


class TestOperationView(TestCase):
    url_name = "operations:form"

    def setUp(self):
        self.nm_mun = "municipio"
        self.p_municipios = mock.patch.object(Municipio.objects, "get_ordered_values")
        self.m_municpios = self.p_municipios.start()
        self.m_municpios.return_value = [{"nm_mun": self.nm_mun}]

        self.p_bairros = mock.patch.object(Bairro.objects, "get_ordered_for_municipio")
        self.m_bairros = self.p_bairros.start()

        self.p_batalhoes = mock.patch.object(Batalhao.objects, "get_ordered_for_municipio")
        self.m_batalhoes = self.p_batalhoes.start()

        self.username = "username"
        self.pwd = "pwd1234"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.url = reverse(self.url_name)

    def tearDown(self):
        self.p_municipios.stop()
        self.p_bairros.stop()
        self.p_batalhoes.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200
        self.m_municpios.assert_called_once_with()
        self.m_bairros.assert_called_once_with(self.nm_mun)
        self.m_batalhoes.assert_called_once_with(self.nm_mun)

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(self.url)

        assert resp.status_code == 302

    def test_uuid_form_hash_on_context(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200
        assert "form_uuid" in resp.context

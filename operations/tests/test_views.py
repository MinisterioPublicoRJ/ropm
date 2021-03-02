import uuid
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from model_bakery import baker

from coredata.models import Bairro, Batalhao, Municipio
from operations.models import Operacao

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


class TestOperationsListView(TestCase):
    url_name = "operations:operations-list"

    def setUp(self):
        self.pwd = "pwd1234"
        self.username = "username"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.operacoes = baker.make(Operacao, usuario=self.user, _quantity=2)

        self.url = reverse(self.url_name)

    @override_settings(OPERATIONS_PER_PAGE=3)
    def test_correct_response(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200
        assert self.operacoes[0] in resp.context["object_list"]
        assert self.operacoes[1] in resp.context["object_list"]

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(self.url)

        assert resp.status_code == 302

    def test_another_user_tries_to_access_operations_list(self):
        another_user = User.objects.create_user(
            username="another",
            password="password"
        )
        self.client.force_login(another_user)

        resp = self.client.get(self.url)

        assert resp.context["object_list"].count() == 0


class TestOperationFormCompleteView(TestCase):
    url_name = "operations:form-complete"

    def setUp(self):
        self.pwd = "pwd1234"
        self.username = "username"

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.client.force_login(self.user)

        self.form_uuid = uuid.uuid4()
        self.operacao = baker.make(
            Operacao,
            usuario=self.user,
            identificador=self.form_uuid,
            _fill_optional=True
        )

        self.url = reverse(self.url_name, kwargs={"form_uuid": self.form_uuid})

    def test_correct_response(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200

    def test_404_if_object_does_not_exists(self):
        url = reverse(self.url_name, kwargs={"form_uuid": uuid.uuid4()})
        resp = self.client.get(url)

        assert resp.status_code == 404

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(self.url)

        assert resp.status_code == 302

    def test_another_user_tries_to_access_form(self):
        another_user = User.objects.create_user(
            username="another",
            password="password"
        )
        self.client.force_login(another_user)

        resp = self.client.get(self.url)

        assert resp.status_code == 404

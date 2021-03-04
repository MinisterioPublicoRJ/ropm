from django.test import TestCase
from model_bakery.recipe import Recipe

from operations.models import Operacao
from operations.serializers import (
    InfoOcorrenciaOneSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoResultadosOperacaoSerializer,
)


class TestInfoOperacionaisOperacaoTwoSerializer(TestCase):
    serializer_class = InfoOperacionaisOperacaoTwoSerializer

    def setUp(self):
        self.data = {
            'tipo_operacao': 'Pl',
            'tipo_acao_repressiva': 'AREP II',
            'numero_ordem_operacoes': '',
            'objetivo_estrategico_operacao': 'Rep',
            'numero_guarnicoes_mobilizadas': 10,
            'numero_policiais_mobilizados': 20
        }

    def test_operacao_planejada_dave_ter_ordem_operacoes(self):
        """Uma operação planejada deve ter uma ordem de operações"""
        ser = self.serializer_class(data=self.data)

        is_valid = ser.is_valid()

        assert not is_valid

    def test_operacao_planejada_com_ordem_operacoes(self):
        """Uma operação planejada deve ter uma ordem de operações"""
        self.data["numero_ordem_operacoes"] = "12345"
        ser = self.serializer_class(data=self.data)

        is_valid = ser.is_valid()

        assert is_valid

    def test_operacao_emergencial_nao_pode_ter_numero_operacoes(self):
        self.data["tipo_operacao"] = "Em"
        self.data["numero_ordem_operacoes"] = "12345"
        ser = self.serializer_class(data=self.data)

        is_valid = ser.is_valid()

        assert not is_valid


class TestInfoResultadosOperacaoSerializer(TestCase):
    serializer_class = InfoResultadosOperacaoSerializer

    def setUp(self):
        self.data = {
            "houve_confronto_daf": True,
            "houve_resultados_operacao": True,
            "houve_ocorrencia_operacao": False,
        }

    def test_unset_houve_ocorrencia_operacao(self):
        """
            Uma operação com ocorrência não pode ser marcada como
            'não houve ocorrência em seguida'
        """
        op = Recipe(Operacao, houve_ocorrencia_operacao=True).prepare()
        ser = self.serializer_class(op, data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid


class TestInfoOcorrenciaOneSerializer(TestCase):
    serializer_class = InfoOcorrenciaOneSerializer

    def setUp(self):
        op = Recipe(Operacao, houve_ocorrencia_operacao=True, _fill_optional=True).prepare()
        self.data = {
            "boletim_ocorrencia_pm": op.boletim_ocorrencia_pm,
            "registro_ocorrencia": "034-00001/2019",
            "nome_comandante_ocorrencia": op.nome_comandante_ocorrencia,
            "rg_pm_comandante_ocorrencia": "12345",
            "posto_comandante_ocorrencia": Operacao.POSTO_COMANDANTE[0][0],
            "houve_apreensao_drogas": op.houve_apreensao_drogas,
            "numero_armas_apreendidas": op.numero_armas_apreendidas,
            "numero_fuzis_apreendidos": op.numero_fuzis_apreendidos,
            "numero_presos": op.numero_presos,
        }

    def test_validate_invalid_registro_ocorrencia(self):
        self.data["registro_ocorrencia"] = "12345"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid

    def test_validate_valid_registro_ocorrencia_1(self):
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert is_valid

    def test_validate_valid_registro_ocorrencia_2(self):
        self.data["registro_ocorrencia"] = "034-00001/2019-01"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert is_valid

    def test_validate_rg_pm_comandante(self):
        self.data["rg_pm_comandante_ocorrencia"] = "abc1234"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid

    def test_validate_posto_comandante(self):
        self.data["posto_comandante_ocorrencia"] = "posto"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid


class TestInfoOperacionaisOperacaoOneSerializer(TestCase):
    serializer_class = InfoOperacionaisOperacaoOneSerializer

    def setUp(self):
        op = Recipe(Operacao, houve_ocorrencia_operacao=True, _fill_optional=True).prepare()
        self.data = {
            "unidade_responsavel": op.unidade_responsavel,
            "unidade_apoiadora": op.unidade_apoiadora,
            "nome_comandante_operacao": op.nome_comandante_operacao,
            "rg_pm_comandante_operacao": "12345",
            "posto_comandante_operacao":Operacao.POSTO_COMANDANTE[0][0],
        }

    def test_validate_valid_rg_pm(self):
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert is_valid

    def test_validate_invalid_rg_pm(self):
        self.data["rg_pm_comandante_operacao"] = "acb1234"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid

    def test_validate_posto_comandante(self):
        self.data["posto_comandante_operacao"] = "posto"
        ser = self.serializer_class(data=self.data)
        is_valid = ser.is_valid()

        assert not is_valid

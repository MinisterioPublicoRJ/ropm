from django.test import TestCase

from operations.serializers import InfoOperacionaisOperacaoTwoSerializer


class TestSerializers(TestCase):
    def test_operacao_planejada_dave_ter_ordem_operacoes(self):
        """Uma operação planejada deve ter uma ordem de operações"""
        data = {
            'tipo_operacao': 'Pl',
            'tipo_acao_repressiva': 'AREP II',
            'numero_ordem_operacoes': '',
            'objetivo_estrategico_operacao': 'Rep',
            'numero_guarnicoes_mobilizadas': 10,
            'numero_policiais_mobilizados': 20
        }
        ser = InfoOperacionaisOperacaoTwoSerializer(data=data)

        is_valid = ser.is_valid()

        assert not is_valid

    def test_operacao_planejada_com_ordem_operacoes(self):
        """Uma operação planejada deve ter uma ordem de operações"""
        data = {
            'tipo_operacao': 'Pl',
            'tipo_acao_repressiva': 'AREP II',
            'numero_ordem_operacoes': '12345',
            'objetivo_estrategico_operacao': 'Rep',
            'numero_guarnicoes_mobilizadas': 10,
            'numero_policiais_mobilizados': 20
        }
        ser = InfoOperacionaisOperacaoTwoSerializer(data=data)

        is_valid = ser.is_valid()

        assert is_valid

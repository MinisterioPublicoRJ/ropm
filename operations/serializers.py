from rest_framework import serializers


class OperacaoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            instance.__setattr__(key, val)

        instance.save()
        return instance


class InfoGeraisOperacaoSerializer(OperacaoSerializer):
    data = serializers.DateField(format="%Y-%m-%d", required=True)
    hora = serializers.TimeField(format="%H:%M:%S", required=True)

    localidade = serializers.CharField(required=True)
    municipio = serializers.CharField(required=True)
    bairro = serializers.CharField(required=True)
    endereco_referencia = serializers.CharField(required=True)
    coordenadas_geo = serializers.CharField(required=False)
    batalhao_responsavel = serializers.CharField(required=True)


class InfoOperacionaisOperacaoOneSerializer(OperacaoSerializer):
    unidade_responsavel = serializers.CharField(required=True)
    unidade_apoiadora = serializers.CharField(allow_blank=True)
    nome_comandante_operacao = serializers.CharField(required=True)
    rg_pm_comandante_operacao = serializers.CharField(required=True)
    posto_comandante_operacao = serializers.CharField(required=True)


class InfoOperacionaisOperacaoTwoSerializer(OperacaoSerializer):
    tipo_operacao = serializers.CharField(required=True)
    tipo_acao_repressiva = serializers.CharField(required=True)
    numero_ordem_operacoes = serializers.CharField(allow_blank=True)
    objetivo_estrategico_operacao = serializers.CharField(required=True)
    numero_guarnicoes_mobilizadas = serializers.IntegerField(required=True)
    numero_policiais_mobilizados = serializers.IntegerField(required=True)


class InfoResultadosOperacaoSerializer(OperacaoSerializer):
    houve_confronto_daf = serializers.BooleanField(required=True)
    houve_resultados_operacao = serializers.BooleanField(required=True)
    houve_ocorrencia_operacao = serializers.BooleanField(required=True)

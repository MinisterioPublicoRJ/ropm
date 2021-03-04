import re

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

    def validate(self, attrs):
        if attrs["tipo_operacao"] == "Pl" and not attrs["numero_ordem_operacoes"]:
            raise serializers.ValidationError(
                {"numero_ordem_operacoes": "Número da ordem deve ser fornecido."}
            )
        return attrs


class InfoResultadosOperacaoSerializer(OperacaoSerializer):
    houve_confronto_daf = serializers.BooleanField(required=True)
    houve_resultados_operacao = serializers.BooleanField(required=True)
    houve_ocorrencia_operacao = serializers.BooleanField(required=True)

    def validate(self, attrs):
        if self.instance.houve_ocorrencia_operacao and not attrs["houve_ocorrencia_operacao"]:
            msg = "Operação com ocorrência não pode ser atualizada para sem ocorrência."
            raise serializers.ValidationError(
                {
                    "houve_ocorrencia_operacao": msg
                }
            )
        return attrs


class InfoOcorrenciaOneSerializer(OperacaoSerializer):
    boletim_ocorrencia_pm = serializers.CharField()
    registro_ocorrencia = serializers.CharField()
    nome_comandante_ocorrencia = serializers.CharField()
    rg_pm_comandante_ocorrencia = serializers.CharField()
    posto_comandante_ocorrencia = serializers.CharField()
    houve_apreensao_drogas = serializers.BooleanField()
    numero_armas_apreendidas = serializers.IntegerField()
    numero_fuzis_apreendidos = serializers.IntegerField()
    numero_presos = serializers.IntegerField()

    def validate_registro_ocorrencia(self, value):
        match = re.match(r"^\d{3}-\d{5}/\d{4}(-\d{2})?$", value)
        if not match:
            raise serializers.ValidationError("Número de RO inválido.")

        return value


class InfoOcorrenciaTwoSerializer(OperacaoSerializer):
    numero_policiais_feridos = serializers.IntegerField()
    numero_baixas_policiais = serializers.IntegerField()
    numero_feridos_por_resistencia = serializers.IntegerField()
    numero_mortes_interv_estado = serializers.IntegerField()
    numero_civis_feridos = serializers.IntegerField()
    numero_civis_mortos_npap = serializers.IntegerField()
    numero_veiculos_recuperados = serializers.IntegerField()
    numero_adolescentes_apreendindos = serializers.IntegerField()

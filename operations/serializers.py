import re

from rest_framework import serializers

from coredata.models import Batalhao, Bairro
from operations.models import Operacao


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

    def validate(self, attrs):
        bairros_validos = Bairro.objects.get_ordered_for_municipio(
            attrs["municipio"]
        ).values_list("bairro", flat=True)
        batalhoes_validos = Batalhao.objects.get_ordered_for_municipio(
            attrs["municipio"]
        ).values_list("bpm", flat=True)

        if attrs["bairro"] not in bairros_validos:
            raise serializers.ValidationError(
                {"bairro": "Bairro inválido para município selecionado."}
            )

        if attrs["batalhao_responsavel"] not in batalhoes_validos:
            raise serializers.ValidationError(
                {"batalhao_responsavel": "Batalhao inválido para município selecionado."}
            )

        return attrs


class InfoADPF635Serializer(OperacaoSerializer):
    justificativa_excepcionalidade_operacao = serializers.CharField(required=True)
    descricao_analise_risco = serializers.CharField(required=True)


class InfoOperacionaisOperacaoOneSerializer(OperacaoSerializer):
    unidade_responsavel = serializers.CharField(required=True)
    unidade_apoiadora = serializers.CharField(allow_blank=True)
    nome_comandante_operacao = serializers.CharField(required=True)
    rg_pm_comandante_operacao = serializers.CharField(required=True)
    posto_comandante_operacao = serializers.CharField(required=True)

    def validate_rg_pm_comandante_operacao(self, value):
        match = re.match(r"\d{5,6}", value)
        if not match:
            raise serializers.ValidationError("Número RG PM inválido.")

        return value

    def validate_posto_comandante_operacao(self, value):
        options = [opt[0] for opt in Operacao.POSTO_COMANDANTE]
        if value not in options:
            raise serializers.ValidationError("Opção inválida.")

        return value


class InfoOperacionaisOperacaoTwoSerializer(OperacaoSerializer):
    tipo_operacao = serializers.CharField(required=True)
    tipo_acao_repressiva = serializers.CharField(required=True)
    numero_ordem_operacoes = serializers.CharField(allow_blank=True)
    objetivo_estrategico_operacao = serializers.CharField(required=True)
    numero_guarnicoes_mobilizadas = serializers.IntegerField(required=True, min_value=0)
    numero_policiais_mobilizados = serializers.IntegerField(required=True, min_value=0)
    numero_veiculos_blindados = serializers.IntegerField(required=True, min_value=0)
    numero_aeronaves = serializers.IntegerField(required=True, min_value=0)

    def validate(self, attrs):
        if attrs["tipo_operacao"] == "Pl" and not attrs["numero_ordem_operacoes"]:
            raise serializers.ValidationError(
                {"numero_ordem_operacoes": "Número da ordem deve ser fornecido."}
            )
        elif attrs["tipo_operacao"] == "Em" and attrs["numero_ordem_operacoes"]:
            raise serializers.ValidationError(
                {
                    "numero_ordem_operacoes":
                    "Número da ordem é apenas para operações planejadas."
                }
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
    numero_armas_apreendidas = serializers.IntegerField(min_value=0)
    numero_fuzis_apreendidos = serializers.IntegerField(min_value=0)
    numero_presos = serializers.IntegerField(min_value=0)

    def validate_posto_comandante_ocorrencia(self, value):
        options = [opt[0] for opt in Operacao.POSTO_COMANDANTE]
        if value not in options:
            raise serializers.ValidationError("Opção inválida.")

        return value

    def validate_registro_ocorrencia(self, value):
        match = re.match(r"^\d{3}-\d{5}/\d{4}(-\d{2})?$", value)
        if not match:
            raise serializers.ValidationError("Número de RO inválido.")

        return value

    def validate_rg_pm_comandante_ocorrencia(self, value):
        match = re.match(r"\d{5,6}", value)
        if not match:
            raise serializers.ValidationError("Número RG PM inválido.")

        return value


class InfoOcorrenciaTwoSerializer(OperacaoSerializer):
    numero_policiais_feridos = serializers.IntegerField(min_value=0)
    numero_mortes_policiais = serializers.IntegerField(min_value=0)
    numero_mortes_interv_estado = serializers.IntegerField(min_value=0)
    numero_civis_feridos = serializers.IntegerField(min_value=0)
    numero_civis_mortos_npap = serializers.IntegerField(min_value=0)
    numero_veiculos_recuperados = serializers.IntegerField(min_value=0)
    numero_adolescentes_apreendidos = serializers.IntegerField(min_value=0)


class GeneralObservationSerializer(OperacaoSerializer):
    observations = serializers.CharField(allow_blank=True)

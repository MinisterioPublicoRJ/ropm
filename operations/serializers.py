from rest_framework import serializers

from operations.models import InformacaoGeralOperacao, InformacaoOperacionalOperacao


class InformacaoGeralOperacaoSerializer(serializers.ModelSerializer):
    hora = serializers.TimeField(format="%H:%M:%S")

    class Meta:
        model = InformacaoGeralOperacao
        exclude = (
            "id",
            "operacao",
        )


class InformacaoOperacionalOperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoOperacionalOperacao
        exclude = (
            "id",
            "operacao",
        )

from rest_framework import serializers

from operations.models import InformacaoGeralOperacao


class InformacaoGeralOperacaoSerializer(serializers.ModelSerializer):
    hora = serializers.TimeField(format="%H:%M:%S")

    class Meta:
        model = InformacaoGeralOperacao
        exclude = ("id", "operacao",)

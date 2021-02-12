from rest_framework.serializers import ModelSerializer

from operations.models import InformacaoGeralOperacao


class InformacaoGeralOperacaoSerializer(ModelSerializer):
    class Meta:
        model = InformacaoGeralOperacao
        exclude = ("operacao",)

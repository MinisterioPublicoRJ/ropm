from rest_framework import serializers

from coredata.models import Bairro, Municipio


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = "__all__"


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = "__all__"

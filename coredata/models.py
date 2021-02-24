from django.db import models


class MunicipioManager(models.Manager):
    def get_ordered_values(self):
        return self.all().order_by("nm_mun").values("cod_6_dig", "nm_mun")


class BairroManager(models.Manager):
    def get_ordered_for_municipio(self, nome_municipio):
        return self.filter(cod_mun__nm_mun=nome_municipio).order_by("bairro")


class BatalhaoManager(models.Manager):
    def get_ordered_for_municipio(self, nome_municipio):
        return self.filter(codigo_mun__nm_mun=nome_municipio).order_by("bpm").distinct()


class Municipio(models.Model):
    objects = MunicipioManager()

    cod_6_dig = models.IntegerField(primary_key=True, db_column="cod_6_dig")
    nm_mun = models.CharField(max_length=60, db_column="nm_mun")
    cod_mun = models.CharField(max_length=7, db_column="cod_mun")

    def __str__(self):
        return self.nm_mun

    class Meta:
        managed = False
        db_table = '"basegeo"."lim_municipios"'


class Bairro(models.Model):
    objects = BairroManager()

    cod_mun = models.ForeignKey(
        Municipio,
        db_column="cod_mun",
        on_delete=models.DO_NOTHING
    )
    municipio = models.TextField(db_column="municipio")
    bairro_id = models.CharField(
        max_length=255,
        primary_key=True,
        db_column="bairro_id"
    )
    bairro = models.TextField(db_column="bairro")

    def __str__(self):
        return f"{self.municipio} - {self.bairro}"

    class Meta:
        managed = False
        db_table = '"bairros"."bairros_rj"'


class Batalhao(models.Model):
    objects = BatalhaoManager()

    id = models.IntegerField(primary_key=True, db_column="id")
    bpm = models.CharField(max_length=50, db_column="bpm")
    codigo_mun = models.ForeignKey(
        Municipio,
        db_column="codigo_mun",
        on_delete=models.DO_NOTHING,
    )
    municipio = models.CharField(max_length=50, db_column="municipio")

    def __str__(self):
        return f"{self.municipio} - {self.bpm}"

    class Meta:
        managed = False
        db_table = '"basegeo"."policia_areas_dps"'


class Delegacia(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column="id")
    nome = models.CharField(max_length=254, db_column="nome")
    cod_mun = models.ForeignKey(
        Municipio,
        db_column="cod_mun",
        on_delete=models.DO_NOTHING,
    )
    municipio = models.CharField(max_length=254, db_column="municipio")

    def __str__(self):
        return f"{self.municipio} - {self.nome}"

    class Meta:
        managed = False
        db_table = '"basegeo_4326"."policia_delegacias"'

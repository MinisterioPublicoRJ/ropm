from django.db import models


class Municipio(models.Model):
    cod_6_dig = models.IntegerField(primary_key=True, db_column="cod_6_dig")
    nm_mun = models.CharField(max_length=60, db_column="nm_mun")
    cod_mun = models.CharField(max_length=7, db_column="cod_mun")

    def __str__(self):
        return self.nm_mun

    class Meta:
        managed = False
        db_table = '"basegeo"."lim_municipios"'


class Bairro(models.Model):
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

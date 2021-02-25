from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

from coredata.models import Bairro, Batalhao, Municipio


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        models = [Bairro, Batalhao, Municipio]
        geo_db = settings.GEO_DATABASE_NAME
        for model in models:
            schema_name = model._meta.db_table.split(".")[0]
            with connections[geo_db].schema_editor(collect_sql=True, atomic=True) as schema_editor:
                sql, params = schema_editor.table_sql(model)
                sql = sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
                with connections[geo_db].cursor() as cursor:
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
                    cursor.execute(sql)

        mun, _ = Municipio.objects.using(geo_db).get_or_create(
            nm_mun="RIO DE JANEIRO",
            cod_6_dig=33045,
            cod_mun="330457",
        )

        Bairro.objects.using(geo_db).get_or_create(
            cod_mun_id=mun.cod_6_dig,
            bairro="CAMPO DOS AFONSOS",
            bairro_id="rio de janeiro158",
        )
        Bairro.objects.using(geo_db).get_or_create(
            cod_mun_id=mun.cod_6_dig,
            bairro="DEODORO",
            bairro_id="rio de janeiro156",
        )

        Batalhao.objects.using(geo_db).get_or_create(
            codigo_mun_id=mun.cod_6_dig,
            bpm="41º BPM",
            id=113,
            municipio="Rio de Janeiro"
        )
        Batalhao.objects.using(geo_db).get_or_create(
            codigo_mun_id=mun.cod_6_dig,
            bpm="9º BPM",
            id=96,
            municipio="Rio de Janeiro"
        )

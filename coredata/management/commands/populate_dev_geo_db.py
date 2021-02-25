from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections


app_label = "coredata"
models = [_ for _ in apps.get_app_config(app_label).get_models()]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        geo_db = settings.GEO_DATABASE_NAME
        for model in models:
            schema_name = model._meta.db_table.split(".")[0]
            with connections[geo_db].schema_editor(collect_sql=True, atomic=True) as schema_editor:
                sql, params = schema_editor.table_sql(model)
                sql = sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
                with connections[geo_db].cursor() as cursor:
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
                    cursor.execute(sql)

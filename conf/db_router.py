from django.conf import settings


class DBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "coredata":
            return settings.GEO_DATABASE_NAME

        return settings.DEFAULT_DATABASE_NAME

    def db_for_write(self, model, **hints):
        return settings.DEFAULT_DATABASE_NAME

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == settings.DEFAULT_DATABASE_NAME

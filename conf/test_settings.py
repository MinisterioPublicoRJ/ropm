from .settings import * # noqa

DATABASES = {
    DEFAULT_DATABASE_NAME: dj_database_url.parse(DATABASE_URL),
}

EMAIL_DEST_NOTIFY = config("EMAIL_DEST_NOTIFY", cast=Csv(), default="dest1,dest2")

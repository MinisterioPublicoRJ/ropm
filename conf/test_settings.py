from .settings import * # noqa

DATABASES = {
    DEFAULT_DATABASE_NAME: dj_database_url.parse(DATABASE_URL),
}
